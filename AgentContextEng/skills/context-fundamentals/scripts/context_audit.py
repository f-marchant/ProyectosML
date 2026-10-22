#!/usr/bin/env python3
"""context-fundamentals: audita un contexto (texto o JSON) por secciones.

Uso:
  python context_audit.py audit ARCHIVO [--window 128000] [--cpt 4] [--priority "texto1,texto2"]
ARCHIVO: .json (lista de {"section":..., "text":...}) o texto/markdown (se divide por encabezados '#').
Solo biblioteca estándar. Los tokens son una ESTIMACION (caracteres / cpt), no un tokenizador real.
"""
import argparse, json, re, sys, hashlib

def load(path):
    raw = open(path, encoding="utf-8").read()
    if path.lower().endswith(".json"):
        data = json.loads(raw)
        return [{"section": str(d.get("section", d.get("role", f"seg{i}"))), "text": str(d.get("text", d.get("content", "")))} for i, d in enumerate(data)]
    parts = re.split(r"(?m)^(?=#{1,3} )", raw)
    out = []
    for i, p in enumerate(x for x in parts if x.strip()):
        title = p.strip().splitlines()[0].lstrip("# ").strip()[:60] or f"seccion{i}"
        out.append({"section": title, "text": p})
    return out

def audit(segs, window, cpt, priority):
    est = lambda t: max(1, round(len(t) / cpt)) if t else 0
    total = sum(est(s["text"]) for s in segs) or 1
    rows, pos = [], 0
    for s in segs:
        t = est(s["text"]); start = pos / total; pos += t; end = pos / total
        rows.append({"section": s["section"], "tokens": t, "share_pct": round(100 * t / total, 1), "span": [round(start, 2), round(end, 2)]})
    seen, dups = {}, []
    for s in segs:
        for para in re.split(r"\n\s*\n", s["text"]):
            para = re.sub(r"(?m)^#{1,6} .*$", "", para)
            k = hashlib.md5(re.sub(r"\s+", " ", para.strip().lower()).encode()).hexdigest()
            if len(para.strip()) > 80:
                if k in seen: dups.append({"section": s["section"], "first_in": seen[k], "preview": para.strip()[:70]})
                else: seen[k] = s["section"]
    full = " ".join(s["text"] for s in segs).lower(); L = max(1, len(full))
    prio = []
    for p in [x.strip().lower() for x in priority if x.strip()]:
        i = full.find(p)
        if i < 0: prio.append({"item": p, "found": False})
        else:
            r = i / L
            prio.append({"item": p, "found": True, "position": round(r, 2), "risk": "lost-in-middle" if 0.3 <= r <= 0.7 else "ok"})
    util = total / window
    recs = []
    if util > 0.8: recs.append("Utilizacion >80%: comprimir u offloadear antes de continuar.")
    elif util > 0.5: recs.append("Utilizacion >50%: planificar compactacion; el rendimiento suele degradarse antes del limite.")
    big = [r for r in rows if r["share_pct"] > 40]
    if big: recs.append("Secciones dominantes (>40%): " + ", ".join(b["section"] for b in big) + ". Evaluar recorte o carga bajo demanda.")
    if dups: recs.append(f"{len(dups)} parrafo(s) duplicado(s): eliminar redundancia.")
    if any(p.get("risk") == "lost-in-middle" for p in prio): recs.append("Mover informacion critica al inicio o al final del contexto.")
    return {"total_tokens_est": total, "window": window, "utilization_pct": round(100 * util, 1),
            "status": "critico" if util > .8 else "atencion" if util > .5 else "saludable",
            "sections": rows, "duplicates": dups, "priority_check": prio, "recommendations": recs}

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("audit"); a.add_argument("file"); a.add_argument("--window", type=int, default=128000)
    a.add_argument("--cpt", type=float, default=4.0); a.add_argument("--priority", default="")
    args = ap.parse_args(argv)
    res = audit(load(args.file), args.window, args.cpt, args.priority.split(","))
    print(json.dumps(res, ensure_ascii=False, indent=2)); return 0

if __name__ == "__main__": sys.exit(main())
