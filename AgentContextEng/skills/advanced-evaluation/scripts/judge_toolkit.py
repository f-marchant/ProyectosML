#!/usr/bin/env python3
"""advanced-evaluation: construye prompts de juez LLM y agrega/valida sus resultados (sin llamar a ningun modelo).

Uso:
  python judge_toolkit.py prompt direct --rubric rubric.json --response resp.txt [--question q.txt] > prompt.txt
  python judge_toolkit.py prompt pairwise --a a.txt --b b.txt [--question q.txt] [--criteria "precision,claridad"] [--swap]
  python judge_toolkit.py aggregate direct jueces.json          # [{"judge":"j1","scores":{"crit":1-5}}], pesos desde --rubric
  python judge_toolkit.py aggregate pairwise runs.json          # [{"order":"AB|BA","winner":"A|B|tie","confidence":0-1}] -> sesgo de posicion
  python judge_toolkit.py agreement humanos.json juez.json      # {"item":score} -> Spearman, Cohen kappa (si categorias), exactitud +-1
rubric.json: {"criteria":[{"name","description","weight","levels":{"1":"...","5":"..."}}]}
"""
import argparse, json, sys
from collections import Counter

def direct_prompt(rub, resp, q):
    lines = ["Eres un evaluador riguroso. Califica la respuesta SOLO con la rubrica. Primero justifica con evidencia citada, despues da el puntaje.", ""]
    if q: lines += ["## Pregunta/tarea", q, ""]
    lines += ["## Respuesta a evaluar", resp, "", "## Rubrica (escala 1-5)"]
    for c in rub["criteria"]:
        lines.append(f"- {c['name']} (peso {c.get('weight', 1)}): {c.get('description', '')}")
        for k, v in sorted(c.get("levels", {}).items()): lines.append(f"    {k}: {v}")
    lines += ["", "No favorezcas respuestas por longitud. Devuelve SOLO JSON:", '{"criteria":[{"name":"...","evidence":"...","score":1,"justification":"..."}],"summary":"..."}']
    return "\n".join(lines)

def pair_prompt(a, b, q, crit, swap):
    if swap: a, b = b, a
    return "\n".join(["Compara dos respuestas. Evalua cada una por separado antes de decidir. No favorezcas por posicion ni longitud.", "",
        *(["## Pregunta/tarea", q, ""] if q else []), "## Respuesta A", a, "", "## Respuesta B", b, "", "## Criterios: " + (crit or "precision, completitud, claridad"), "",
        'Devuelve SOLO JSON: {"analysis_a":"...","analysis_b":"...","winner":"A|B|tie","confidence":0.0}'])

def agg_direct(judges, rub):
    w = {c["name"]: c.get("weight", 1) for c in rub["criteria"]} if rub else None
    names = sorted({k for j in judges for k in j["scores"]}); per = {}
    for n in names:
        v = [j["scores"][n] for j in judges if n in j["scores"]]; m = sum(v) / len(v)
        per[n] = {"mean": round(m, 2), "min": min(v), "max": max(v), "spread": max(v) - min(v)}
    ww = {n: (w or {}).get(n, 1) for n in names}; tot = sum(ww.values())
    return {"judges": len(judges), "per_criterion": per, "weighted_score": round(sum(per[n]["mean"] * ww[n] for n in names) / tot, 2),
            "disagreement": [n for n in names if per[n]["spread"] >= 2]}

def agg_pair(runs):
    res = Counter()
    for r in runs:
        win = r["winner"]
        if win == "tie": res["tie"] += 1
        else:
            real = win if r.get("order", "AB") == "AB" else ("B" if win == "A" else "A"); res[real] += 1
    n = len(runs); a_first = [r for r in runs if r.get("order", "AB") == "AB"]; b_first = [r for r in runs if r.get("order") == "BA"]
    pos_pref = sum(1 for r in runs if r["winner"] == "A") / n
    consistent = None
    if a_first and b_first:
        ra = Counter(r["winner"] for r in a_first); rb = Counter(("B" if r["winner"] == "A" else "A" if r["winner"] == "B" else "tie") for r in b_first)
        consistent = ra.most_common(1)[0][0] == rb.most_common(1)[0][0]
    final = res.most_common(1)[0][0]
    return {"runs": n, "tally_real_labels": dict(res), "winner": final, "first_position_win_rate": round(pos_pref, 2),
            "position_bias_suspected": bool(pos_pref > 0.7 or pos_pref < 0.3) if n >= 4 else None, "consistent_across_orders": consistent,
            "mean_confidence": round(sum(r.get("confidence", 0) for r in runs) / n, 2)}

def rank(v):
    s = sorted(range(len(v)), key=lambda i: v[i]); r = [0.0] * len(v); i = 0
    while i < len(s):
        j = i
        while j + 1 < len(s) and v[s[j + 1]] == v[s[i]]: j += 1
        for k in range(i, j + 1): r[s[k]] = (i + j) / 2 + 1
        i = j + 1
    return r

def pearson(x, y):
    mx, my = sum(x) / len(x), sum(y) / len(y); sx = sum((a - mx) ** 2 for a in x) ** .5; sy = sum((b - my) ** 2 for b in y) ** .5
    return None if sx == 0 or sy == 0 else sum((a - mx) * (b - my) for a, b in zip(x, y)) / (sx * sy)

def kappa(a, b):
    n = len(a); po = sum(x == y for x, y in zip(a, b)) / n; ca, cb = Counter(a), Counter(b)
    pe = sum(ca[k] * cb.get(k, 0) for k in ca) / n ** 2
    return None if pe == 1 else (po - pe) / (1 - pe)

def agreement(h, j):
    ids = sorted(set(h) & set(j)); x = [h[i] for i in ids]; y = [j[i] for i in ids]
    sp = pearson(rank(x), rank(y)); kp = kappa([round(v) for v in x], [round(v) for v in y])
    return {"n": len(ids), "spearman": None if sp is None else round(sp, 3), "cohen_kappa": None if kp is None else round(kp, 3),
            "within_1_pct": round(100 * sum(abs(a - b) <= 1 for a, b in zip(x, y)) / len(ids), 1), "mean_bias_judge_minus_human": round(sum(b - a for a, b in zip(x, y)) / len(ids), 2),
            "reading": "alineado" if sp is not None and sp >= 0.8 else "parcial" if sp is not None and sp >= 0.5 else "insuficiente: recalibrar rubrica"}

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("prompt"); p.add_argument("kind", choices=["direct", "pairwise"]); p.add_argument("--rubric"); p.add_argument("--response"); p.add_argument("--a"); p.add_argument("--b")
    p.add_argument("--question"); p.add_argument("--criteria", default=""); p.add_argument("--swap", action="store_true")
    g = sub.add_parser("aggregate"); g.add_argument("kind", choices=["direct", "pairwise"]); g.add_argument("file"); g.add_argument("--rubric")
    h = sub.add_parser("agreement"); h.add_argument("human"); h.add_argument("judge")
    a = ap.parse_args(argv); rd = lambda f: open(f, encoding="utf-8").read()
    if a.cmd == "prompt":
        q = rd(a.question) if a.question else ""
        print(direct_prompt(json.load(open(a.rubric)), rd(a.response), q) if a.kind == "direct" else pair_prompt(rd(a.a), rd(a.b), q, a.criteria, a.swap))
    elif a.cmd == "aggregate":
        d = json.load(open(a.file)); out = agg_direct(d, json.load(open(a.rubric)) if a.rubric else None) if a.kind == "direct" else agg_pair(d)
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else: print(json.dumps(agreement(json.load(open(a.human)), json.load(open(a.judge))), indent=2))
    return 0

if __name__ == "__main__": sys.exit(main())
