#!/usr/bin/env python3
"""context-compression: evalua un resumen/compactacion contra el original.

Uso:
  python compression_eval.py extract ORIGINAL            # extrae artefactos (archivos, URLs, decisiones, errores, TODO)
  python compression_eval.py score ORIGINAL RESUMEN [--probes probes.json] [--cpt 4]
probes.json: [{"question":"...","expected":["kw1","kw2"]}]  (retencion = % de palabras clave presentes)
Mide: razon de compresion, retencion de artefactos y retencion por sondas. Sin LLM: heuristicas deterministas.
"""
import argparse, json, re, sys

PATH = r"(?:[\w.\-]+/)+[\w.\-]+\.\w{1,6}|\b[\w\-]+\.(?:py|js|ts|md|json|ya?ml|csv|txt|sql|sh|docx|xlsx|pptx)\b"

def extract(text):
    return {
        "files": sorted(set(re.findall(PATH, text))),
        "urls": sorted(set(re.findall(r"https?://[^\s)>\]]+", text))),
        "decisions": [m.strip() for m in re.findall(r"(?im)^.*\b(?:decid\w+|decision|decided|chose|elegimos|acordamos|we will)\b.*$", text)][:25],
        "errors": [m.strip() for m in re.findall(r"(?im)^.*\b(?:error|exception|failed|fallo|traceback)\b.*$", text)][:25],
        "todos": [m.strip() for m in re.findall(r"(?im)^.*\b(?:todo|next|pendiente|siguiente paso)\b.*$", text)][:25],
        "numbers": sorted(set(re.findall(r"\b\d+(?:[.,]\d+)?%?\b", text)))[:60],
    }

def score(orig, summ, probes, cpt):
    ex = extract(orig); low = summ.lower(); detail = {}
    for k in ("files", "urls"):
        items = ex[k]; kept = [i for i in items if i.lower() in low]
        detail[k] = {"total": len(items), "kept": len(kept), "retention": round(len(kept) / len(items), 2) if items else None, "missing": [i for i in items if i not in kept][:10]}
    for k in ("decisions", "errors", "todos"):
        items = ex[k]; kept = 0
        for it in items:
            words = {w for w in re.findall(r"\w{5,}", it.lower())}
            if words and len(words & set(re.findall(r"\w{5,}", low))) / len(words) >= 0.5: kept += 1
        detail[k] = {"total": len(items), "kept": kept, "retention": round(kept / len(items), 2) if items else None}
    pr = []
    for p in probes:
        exp = [e.lower() for e in p.get("expected", [])]; hit = [e for e in exp if e in low]
        pr.append({"question": p.get("question", ""), "retention": round(len(hit) / len(exp), 2) if exp else None, "missing": [e for e in exp if e not in hit]})
    vals = [d["retention"] for d in detail.values() if d["retention"] is not None] + [x["retention"] for x in pr if x["retention"] is not None]
    ot, st = len(orig) / cpt, len(summ) / cpt
    return {"original_tokens_est": round(ot), "summary_tokens_est": round(st), "compression_ratio": round(ot / max(st, 1), 2),
            "overall_retention": round(sum(vals) / len(vals), 2) if vals else None, "artifacts": detail, "probes": pr,
            "warning": "Retencion baja: riesgo de re-lectura (mas tokens por tarea)." if vals and sum(vals) / len(vals) < 0.7 else None}

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    e = sub.add_parser("extract"); e.add_argument("original")
    s = sub.add_parser("score"); s.add_argument("original"); s.add_argument("summary"); s.add_argument("--probes"); s.add_argument("--cpt", type=float, default=4.0)
    a = ap.parse_args(argv); rd = lambda p: open(p, encoding="utf-8").read()
    if a.cmd == "extract": out = extract(rd(a.original))
    else: out = score(rd(a.original), rd(a.summary), json.load(open(a.probes)) if a.probes else [], a.cpt)
    print(json.dumps(out, ensure_ascii=False, indent=2)); return 0

if __name__ == "__main__": sys.exit(main())
