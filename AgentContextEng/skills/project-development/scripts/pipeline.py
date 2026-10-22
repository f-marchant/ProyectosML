#!/usr/bin/env python3
"""project-development: pipeline por etapas con cache en archivos (acquire -> prepare -> process -> parse -> render).

Como el sandbox no tiene red ni LLM, la etapa 'process' funciona en modo manual:
  1) prepare genera prompts/<id>.txt   2) TU (o Copilot) escribes responses/<id>.txt   3) parse valida, 4) render consolida.
Uso:
  python pipeline.py init --root proyecto [--template "Resume en JSON con claves {keys}: {text}"] --keys titulo,resumen
  python pipeline.py acquire --root proyecto ARCHIVO_O_CARPETA      # copia items a raw/ (uno por archivo; .jsonl = un item por linea)
  python pipeline.py prepare|parse|render|status --root proyecto
  python pipeline.py estimate --root proyecto --price-in 3 --price-out 15 [--out-ratio 0.3]   # USD por millon de tokens
Idempotente: no rehace etapas cuyo archivo de salida ya existe (usa --force para rehacer).
"""
import argparse, glob, json, os, re, shutil, sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR.parent.parent / "_shared"))
from safe_io import atomic_write_json, atomic_write_text, load_json

def P(root, *a): return os.path.join(root, *a)
def cfg(root): return load_json(P(root, "config.json"))
def est(t): return max(1, round(len(t) / 4))

def init(a):
    for d in ("raw", "prompts", "responses", "parsed", "out"): os.makedirs(P(a.root, d), exist_ok=True)
    atomic_write_json(P(a.root, "config.json"), {"template": a.template, "keys": [k for k in a.keys.split(",") if k]})
    print(f"proyecto listo en {a.root}")

def acquire(a):
    n = 0
    srcs = [a.src] if os.path.isfile(a.src) else sorted(glob.glob(P(a.src, "*")))
    for s in srcs:
        base = os.path.splitext(os.path.basename(s))[0]
        if s.endswith(".jsonl"):
            for i, l in enumerate(open(s, encoding="utf-8")):
                if l.strip(): atomic_write_text(P(a.root, "raw", f"{base}_{i:04d}.txt"), json.loads(l).get("text", l)); n += 1
        else: shutil.copy(s, P(a.root, "raw", base + ".txt")); n += 1
    print(f"{n} items en raw/")

def prepare(a):
    c = cfg(a.root); n = 0
    for f in sorted(glob.glob(P(a.root, "raw", "*.txt"))):
        i = os.path.basename(f); o = P(a.root, "prompts", i)
        if os.path.exists(o) and not a.force: continue
        atomic_write_text(o, c["template"].replace("{keys}", ", ".join(c["keys"])).replace("{text}", open(f, encoding="utf-8").read())); n += 1
    print(f"{n} prompts generados en prompts/ (escribe respuestas en responses/ con el mismo nombre)")

def extract_json(t):
    t = re.sub(r"^```(?:json)?|```$", "", t.strip(), flags=re.M).strip()
    try: return json.loads(t)
    except Exception:
        m = re.search(r"\{.*\}", t, re.S)
        return json.loads(m.group(0)) if m else None

def parse(a):
    c = cfg(a.root); ok = bad = 0; errs = []
    for f in sorted(glob.glob(P(a.root, "responses", "*.txt"))):
        i = os.path.basename(f)[:-4]
        try: obj = extract_json(open(f, encoding="utf-8").read())
        except Exception as e: obj = None
        miss = [k for k in c["keys"] if not obj or k not in obj] if obj is not None else c["keys"]
        if obj is None or miss: bad += 1; errs.append({"id": i, "missing": miss}); continue
        atomic_write_json(P(a.root, "parsed", i + ".json"), obj); ok += 1
    print(json.dumps({"parsed_ok": ok, "invalid": bad, "errors": errs}, ensure_ascii=False, indent=1))

def render(a):
    c = cfg(a.root); rows = []
    for f in sorted(glob.glob(P(a.root, "parsed", "*.json"))): rows.append((os.path.basename(f)[:-5], json.load(open(f, encoding="utf-8"))))
    md = ["| id | " + " | ".join(c["keys"]) + " |", "|---|" + "---|" * len(c["keys"])]
    md += ["| " + i + " | " + " | ".join(str(o.get(k, "")).replace("|", "/").replace("\n", " ") for k in c["keys"]) + " |" for i, o in rows]
    atomic_write_text(P(a.root, "out", "report.md"), "\n".join(md)); atomic_write_json(P(a.root, "out", "report.json"), [{"id": i, **o} for i, o in rows])
    print(f"{len(rows)} filas -> out/report.md y out/report.json")

def status(a):
    cnt = lambda d, e="txt": len(glob.glob(P(a.root, d, "*." + e)))
    print(json.dumps({"raw": cnt("raw"), "prompts": cnt("prompts"), "responses": cnt("responses"), "parsed": cnt("parsed", "json")}))

def estimate(a):
    ti = sum(est(open(f, encoding="utf-8").read()) for f in glob.glob(P(a.root, "prompts", "*.txt")))
    to = round(ti * a.out_ratio); cost = ti / 1e6 * a.price_in + to / 1e6 * a.price_out
    print(json.dumps({"items": len(glob.glob(P(a.root, "prompts", "*.txt"))), "input_tokens_est": ti, "output_tokens_est": to, "cost_usd_est": round(cost, 4)}))

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for n in ("init", "acquire", "prepare", "parse", "render", "status", "estimate"):
        s = sub.add_parser(n); s.add_argument("--root", required=True); s.add_argument("--force", action="store_true")
        if n == "init": s.add_argument("--template", default="Extrae {keys} del texto y responde SOLO JSON.\n\nTexto:\n{text}"); s.add_argument("--keys", default="titulo,resumen")
        if n == "acquire": s.add_argument("src")
        if n == "estimate": s.add_argument("--price-in", type=float, default=3.0); s.add_argument("--price-out", type=float, default=15.0); s.add_argument("--out-ratio", type=float, default=0.3)
    a = ap.parse_args(argv); globals()[a.cmd](a); return 0

if __name__ == "__main__": sys.exit(main())
