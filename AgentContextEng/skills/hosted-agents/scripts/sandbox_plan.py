#!/usr/bin/env python3
"""hosted-agents: dimensionamiento y planificacion de infraestructura de agentes hospedados (calculos reales, sin red).

Uso:
  python sandbox_plan.py pool-size --arrivals-per-min 6 --warm-minutes 2 [--target 0.99] [--max-pool 500]
  python sandbox_plan.py latency --budget-s 5 --parts "clone=2.5,deps=3,model_ttft=0.8,boot=1.2"
  python sandbox_plan.py image-schedule --commits-per-day 40 --build-minutes 12 --max-staleness-min 30
  python sandbox_plan.py cost --sessions-per-day 200 --session-minutes 25 --price-per-hour 0.35 --idle-pool 4
  python sandbox_plan.py dockerfile CONFIG.json    # {"base":"python:3.12-slim","apt":[...],"pip":[...],"repos":[{"url","path"}],"setup":[...],"workdir":"/work"}
pool-size usa demanda Poisson (lambda = llegadas/min * minutos de calentamiento) y el cuantil objetivo.
"""
import argparse, json, math, re, sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR.parent.parent / "_shared"))
from safe_io import SafeIOError, require_finite_nonnegative

SAFE_TOKEN = re.compile(r"^[A-Za-z0-9_./:@+=,-]+$")
SAFE_IMAGE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.:/-]*$")


def safe_token(value, field):
    if not isinstance(value, str) or not value or "\n" in value or not SAFE_TOKEN.fullmatch(value):
        raise SafeIOError(f"{field} contiene caracteres no permitidos")
    return value


def validate_config(c, allow_setup):
    base = safe_token(c.get("base", "ubuntu:24.04"), "base")
    if not SAFE_IMAGE.fullmatch(base):
        raise SafeIOError("base no es una imagen valida")
    for field in ("apt", "pip"):
        values = c.get(field, [])
        if not isinstance(values, list):
            raise SafeIOError(f"{field} debe ser una lista")
        for value in values:
            safe_token(value, f"{field}[]")
    for repo in c.get("repos", []):
        if not isinstance(repo, dict) or not isinstance(repo.get("url"), str) or not re.fullmatch(r"https?://[^\s<>\"']+", repo["url"]):
            raise SafeIOError("cada repo requiere una URL HTTP(S) valida")
        safe_token(repo.get("path", "."), "repos[].path")
    setup = c.get("setup", [])
    if setup and not allow_setup:
        raise SafeIOError("setup contiene comandos; reejecuta con --allow-setup solo tras revisar la configuracion")
    if not isinstance(setup, list) or any(not isinstance(value, str) or "\n" in value for value in setup):
        raise SafeIOError("setup debe ser una lista de comandos de una linea")
    workdir = c.get("workdir", "/work")
    if not isinstance(workdir, str) or "\n" in workdir or not workdir.startswith("/") or any(ch in workdir for ch in (";", "&", "|", "`", "$")):
        raise SafeIOError("workdir debe ser una ruta absoluta sin metacaracteres")

def poisson_quantile(lam, q, cap):
    p = math.exp(-lam); c = p; k = 0
    while c < q and k < cap: k += 1; p *= lam / k; c += p
    return k

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    a_ = sub.add_parser("pool-size"); a_.add_argument("--arrivals-per-min", type=float, required=True); a_.add_argument("--warm-minutes", type=float, required=True); a_.add_argument("--target", type=float, default=0.99); a_.add_argument("--max-pool", type=int, default=500)
    l_ = sub.add_parser("latency"); l_.add_argument("--budget-s", type=float, required=True); l_.add_argument("--parts", required=True)
    i_ = sub.add_parser("image-schedule"); i_.add_argument("--commits-per-day", type=float, required=True); i_.add_argument("--build-minutes", type=float, required=True); i_.add_argument("--max-staleness-min", type=float, required=True)
    c_ = sub.add_parser("cost"); c_.add_argument("--sessions-per-day", type=float, required=True); c_.add_argument("--session-minutes", type=float, required=True); c_.add_argument("--price-per-hour", type=float, required=True); c_.add_argument("--idle-pool", type=int, default=0)
    d_ = sub.add_parser("dockerfile"); d_.add_argument("file"); d_.add_argument("--allow-setup", action="store_true", help="permite emitir comandos setup tras revision humana")
    a = ap.parse_args(argv)
    try:
        if a.cmd == "pool-size":
            require_finite_nonnegative(a.arrivals_per_min, "arrivals-per-min")
            require_finite_nonnegative(a.warm_minutes, "warm-minutes")
            if not 0 <= a.target <= 1:
                raise SafeIOError("target debe estar entre 0 y 1")
            if a.max_pool < 1:
                raise SafeIOError("max-pool debe ser positivo")
            lam = a.arrivals_per_min * a.warm_minutes; n = poisson_quantile(lam, a.target, a.max_pool)
            out = {"expected_concurrent_warmups": round(lam, 2), "pool_size": n, "target_hit_probability": a.target, "note": "Si la tasa varia por hora, calcular con el pico."}
        elif a.cmd == "latency":
            require_finite_nonnegative(a.budget_s, "budget-s")
            parts = {}
            for item in a.parts.split(","):
                pair = item.split("=", 1)
                if len(pair) != 2 or not pair[0]:
                    raise SafeIOError("parts debe usar formato nombre=segundos")
                parts[pair[0]] = require_finite_nonnegative(float(pair[1]), f"parts[{pair[0]}]")
            tot = sum(parts.values())
            if not tot:
                raise SafeIOError("parts debe contener al menos un valor positivo")
            out = {"total_s": round(tot, 2), "budget_s": a.budget_s, "within_budget": tot <= a.budget_s, "over_by_s": round(max(0, tot - a.budget_s), 2),
                   "largest_first": sorted(({"step": k, "s": v, "share_pct": round(100 * v / tot, 1)} for k, v in parts.items()), key=lambda x: -x["s"]),
                   "advice": "Mover pasos de preparacion (clone, deps, boot) a la imagen precalentada; dejar solo el TTFT del modelo en la ruta del usuario." if tot > a.budget_s else "Dentro de presupuesto."}
        elif a.cmd == "image-schedule":
            for name in ("commits_per_day", "build_minutes", "max_staleness_min"):
                require_finite_nonnegative(getattr(a, name), name)
            interval = min(a.max_staleness_min - a.build_minutes, a.max_staleness_min)
            feasible = interval > 0; builds = round(1440 / max(interval, 1)) if feasible else None
            out = {"feasible": feasible, "rebuild_every_min": max(1, round(interval)) if feasible else None, "builds_per_day": builds, "build_hours_per_day": round(builds * a.build_minutes / 60, 1) if builds else None,
                   "cron": f"*/{max(1, round(interval))} * * * *" if feasible and interval < 60 else None, "commits_between_builds_avg": round(a.commits_per_day / 1440 * max(interval, 0), 1),
                   "warning": None if feasible else "El tiempo de build supera la obsolescencia maxima: acelerar el build o relajar el limite."}
        elif a.cmd == "cost":
            for name in ("sessions_per_day", "session_minutes", "price_per_hour"):
                require_finite_nonnegative(getattr(a, name), name)
            if a.idle_pool < 0:
                raise SafeIOError("idle-pool no puede ser negativo")
            run = a.sessions_per_day * a.session_minutes / 60 * a.price_per_hour; idle = a.idle_pool * 24 * a.price_per_hour
            out = {"session_cost_day": round(run, 2), "idle_pool_cost_day": round(idle, 2), "total_day": round(run + idle, 2), "total_month_30d": round(30 * (run + idle), 2), "idle_share_pct": round(100 * idle / (run + idle), 1) if run + idle else 0}
        else:
            with open(a.file, encoding="utf-8") as handle:
                c = json.load(handle)
            validate_config(c, a.allow_setup)
            L = [f"FROM {c.get('base', 'ubuntu:24.04')}", "ENV DEBIAN_FRONTEND=noninteractive"]
            if c.get("apt"): L.append("RUN apt-get update && apt-get install -y --no-install-recommends " + " ".join(c["apt"]) + " git ca-certificates && rm -rf /var/lib/apt/lists/*")
            L.append(f"WORKDIR {c.get('workdir', '/work')}")
            for r in c.get("repos", []): L.append(f"RUN git clone --depth 1 {r['url']} {r.get('path', '.')}")
            if c.get("pip"): L.append("RUN pip install --no-cache-dir " + " ".join(c["pip"]))
            for s in c.get("setup", []): L.append(f"RUN {s}")
            L.append('CMD ["sleep", "infinity"]'); print("\n".join(L)); return 0
        print(json.dumps(out, ensure_ascii=False, indent=2)); return 0
    except (OSError, ValueError, json.JSONDecodeError, SafeIOError) as exc:
        print(f"error: {exc}", file=sys.stderr); return 2

if __name__ == "__main__": sys.exit(main())
