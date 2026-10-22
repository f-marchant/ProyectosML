#!/usr/bin/env python3
"""evaluation: ejecuta verificaciones deterministicas y rubricas sobre salidas de un agente.

Uso:
  python eval_runner.py run TESTS.json SALIDAS.json [--threshold 0.7] [--out reporte.json]
  python eval_runner.py compare BASE.json NUEVO.json [--tolerance 0.02]     # regresiones entre dos reportes
TESTS.json: {"rubric":{"dim":peso,...}, "tests":[{"id","input","checks":[{"type":"contains|not_contains|regex|json_valid|max_chars|min_chars|equals","value":...}],
             "scores":{"dim":0-1}  # opcional: puntajes de rubrica de un humano/LLM juez}]}
SALIDAS.json: {"<id>": "texto de salida"}  o  [{"id","output"}]
"""
import argparse, json, re, sys

def run_check(c, out):
    t, v = c["type"], c.get("value")
    if t == "contains": return str(v).lower() in out.lower()
    if t == "not_contains": return str(v).lower() not in out.lower()
    if t == "equals": return out.strip() == str(v).strip()
    if t == "regex": return re.search(v, out, re.S) is not None
    if t == "max_chars": return len(out) <= int(v)
    if t == "min_chars": return len(out) >= int(v)
    if t == "json_valid":
        try: json.loads(out); return True
        except Exception: return False
    raise ValueError(f"check desconocido: {t}")

def run(spec, outputs, threshold):
    if isinstance(outputs, list): outputs = {o["id"]: o["output"] for o in outputs}
    rubric = spec.get("rubric", {}); res = []
    for t in spec["tests"]:
        out = outputs.get(t["id"])
        if out is None: res.append({"id": t["id"], "status": "missing", "score": 0.0}); continue
        chk = [{"type": c["type"], "value": c.get("value"), "pass": run_check(c, out)} for c in t.get("checks", [])]
        det = sum(c["pass"] for c in chk) / len(chk) if chk else None
        rub = None
        if t.get("scores") and rubric:
            w = sum(rubric.values()); rub = sum(rubric[d] * t["scores"].get(d, 0) for d in rubric) / w
        parts = [x for x in (det, rub) if x is not None]
        sc = sum(parts) / len(parts) if parts else 0.0
        res.append({"id": t["id"], "status": "pass" if sc >= threshold else "fail", "score": round(sc, 3), "deterministic": det, "rubric": None if rub is None else round(rub, 3), "failed_checks": [c for c in chk if not c["pass"]]})
    sc = [r["score"] for r in res]
    return {"threshold": threshold, "n": len(res), "passed": sum(r["status"] == "pass" for r in res), "mean_score": round(sum(sc) / len(sc), 3) if sc else 0, "results": res}

def compare(base, new, tol):
    b = {r["id"]: r["score"] for r in base["results"]}; n = {r["id"]: r["score"] for r in new["results"]}
    reg = [{"id": i, "before": b[i], "after": n[i]} for i in b if i in n and n[i] < b[i] - tol]
    imp = [{"id": i, "before": b[i], "after": n[i]} for i in b if i in n and n[i] > b[i] + tol]
    return {"mean_before": base["mean_score"], "mean_after": new["mean_score"], "regressions": reg, "improvements": imp, "verdict": "REGRESION" if reg else "OK"}

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run"); r.add_argument("tests"); r.add_argument("outputs"); r.add_argument("--threshold", type=float, default=0.7); r.add_argument("--out")
    c = sub.add_parser("compare"); c.add_argument("base"); c.add_argument("new"); c.add_argument("--tolerance", type=float, default=0.02)
    a = ap.parse_args(argv)
    if a.cmd == "run":
        rep = run(json.load(open(a.tests)), json.load(open(a.outputs)), a.threshold)
        if a.out: json.dump(rep, open(a.out, "w"), indent=2)
    else: rep = compare(json.load(open(a.base)), json.load(open(a.new)), a.tolerance)
    print(json.dumps(rep, ensure_ascii=False, indent=2)); return 0

if __name__ == "__main__": sys.exit(main())
