#!/usr/bin/env python3
"""self-improvement-loops: compuerta de aceptacion para cambios autogenerados, tamano de edicion y seleccion de poblacion.

Uso:
  python loop_gate.py gate RESULTADOS.json [--seed 7] [--boot 2000] [--max-gap 0.15]
  python loop_gate.py diffsize ANTES.txt DESPUES.txt [--max-ratio 0.2]
  python loop_gate.py select POBLACION.json [--k 3] [--diversity 0.3]
RESULTADOS.json: {"incumbent":{"dev":{"t1":1,"t2":0,...},"train":{...},"cost":n},"candidate":{...},"protected":["t1","t7"]}
Regla (SE pareado): d = acc_cand - acc_inc; pasa si d > SE; falla si d < -SE; dentro de 1 SE solo pasa si el costo es menor.
Ademas: IC bootstrap 95%, regresion en tareas protegidas y brecha train-dev (sobreajuste).
POBLACION.json: [{"id","score","genome":"texto o lista de tokens"}]
"""
import argparse, difflib, json, math, random, re, sys

def mean(v): return sum(v) / len(v) if v else 0.0

def gate(r, seed, boot, max_gap):
    inc, cand = r["incumbent"], r["candidate"]; dev_i, dev_c = inc["dev"], cand["dev"]; ids = sorted(set(dev_i) & set(dev_c))
    if len(ids) < 2: return {"error": "se requieren >=2 tareas dev comunes"}
    diffs = [dev_c[i] - dev_i[i] for i in ids]; d = mean(diffs); n = len(diffs)
    var = sum((x - d) ** 2 for x in diffs) / (n - 1); se = math.sqrt(var / n)
    rnd = random.Random(seed); bs = sorted(mean([rnd.choice(diffs) for _ in range(n)]) for _ in range(boot)); lo, hi = bs[int(.025 * boot)], bs[int(.975 * boot) - 1]
    cost_i, cost_c = inc.get("cost"), cand.get("cost"); cheaper = cost_i is not None and cost_c is not None and cost_c < cost_i
    verdict = "pass" if d > se else "fail" if d < -se else ("pass" if cheaper else "tie-reject")
    prot = [p for p in r.get("protected", []) if p in dev_i and p in dev_c and dev_c[p] < dev_i[p]]
    gap = None; warn = []
    if cand.get("train") and cand.get("dev"):
        gap = mean(list(cand["train"].values())) - mean(list(cand["dev"].values()))
        if gap > max_gap: warn.append(f"Brecha train-dev {gap:.2f} > {max_gap}: posible sobreajuste.")
    if prot: verdict = "fail"; warn.append(f"Regresion en tareas protegidas: {prot}.")
    if n < 20: warn.append("Pocas tareas dev (<20): el IC es poco fiable.")
    return {"n_dev_tasks": n, "delta": round(d, 4), "se": round(se, 4), "ci95": [round(lo, 4), round(hi, 4)], "ci_excludes_zero": lo > 0 or hi < 0, "incumbent_acc": round(mean([dev_i[i] for i in ids]), 4), "candidate_acc": round(mean([dev_c[i] for i in ids]), 4),
            "cost_incumbent": cost_i, "cost_candidate": cost_c, "protected_regressions": prot, "train_dev_gap": None if gap is None else round(gap, 4), "warnings": warn, "verdict": verdict}

def diffsize(a, b, max_ratio):
    A, B = a.splitlines(), b.splitlines(); sm = difflib.SequenceMatcher(None, A, B); ch = 0
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag != "equal": ch += max(i2 - i1, j2 - j1)
    ratio = ch / max(len(A), 1)
    return {"lines_before": len(A), "lines_after": len(B), "changed_lines": ch, "change_ratio": round(ratio, 3), "max_ratio": max_ratio, "within_bound": ratio <= max_ratio, "verdict": "aceptable" if ratio <= max_ratio else "edicion demasiado grande: dividir en cambios acotados"}

def toks(g): return set(g) if isinstance(g, list) else set(re.findall(r"\w+", str(g).lower()))

def select(pop, k, div):
    chosen = []; rest = sorted(pop, key=lambda p: -p["score"])
    while rest and len(chosen) < k:
        pick = None
        for c in rest:
            if all(1 - (len(toks(c["genome"]) & toks(x["genome"])) / max(1, len(toks(c["genome"]) | toks(x["genome"])))) >= div for x in chosen): pick = c; break
        pick = pick or rest[0]; chosen.append(pick); rest.remove(pick)
    return {"selected": [{"id": c["id"], "score": c["score"]} for c in chosen], "diversity_threshold": div}

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    g = sub.add_parser("gate"); g.add_argument("file"); g.add_argument("--seed", type=int, default=7); g.add_argument("--boot", type=int, default=2000); g.add_argument("--max-gap", type=float, default=0.15)
    d = sub.add_parser("diffsize"); d.add_argument("before"); d.add_argument("after"); d.add_argument("--max-ratio", type=float, default=0.2)
    s = sub.add_parser("select"); s.add_argument("file"); s.add_argument("--k", type=int, default=3); s.add_argument("--diversity", type=float, default=0.3)
    a = ap.parse_args(argv); rd = lambda p: open(p, encoding="utf-8").read()
    out = gate(json.load(open(a.file)), a.seed, a.boot, a.max_gap) if a.cmd == "gate" else diffsize(rd(a.before), rd(a.after), a.max_ratio) if a.cmd == "diffsize" else select(json.load(open(a.file)), a.k, a.diversity)
    print(json.dumps(out, ensure_ascii=False, indent=2)); return 0

if __name__ == "__main__": sys.exit(main())
