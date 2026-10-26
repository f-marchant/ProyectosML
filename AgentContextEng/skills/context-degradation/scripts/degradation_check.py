#!/usr/bin/env python3
"""context-degradation: detecta senales de degradacion en un contexto de texto.

Uso:
  python degradation_check.py check ARCHIVO [--facts "dato1,dato2"] [--window 128000] [--cpt 4]
Detecta: parrafos repetidos (distraccion/envenenamiento por repeticion), valores contradictorios
para la misma clave ('clave: valor' o 'clave = valor') y afirmaciones opuestas (clash),
posicion de datos criticos (lost-in-the-middle) y tamano relativo a la ventana.
"""
import argparse, json, re, sys
from collections import defaultdict

def norm(s): return re.sub(r"\s+", " ", s.strip().lower())

def check(text, facts, window, cpt):
    paras = [p for p in re.split(r"\n\s*\n", text) if p.strip()]
    seen, repeats = {}, []
    for i, p in enumerate(paras):
        k = norm(p)
        if len(k) > 60:
            if k in seen: repeats.append({"paragraph": i, "same_as": seen[k], "preview": p.strip()[:70]})
            else: seen[k] = i
    kv = defaultdict(list)
    for ln_no, ln in enumerate(text.splitlines(), 1):
        m = re.match(r"\s*[-*]?\s*([A-Za-z_][\w \-]{1,40}?)\s*[:=]\s*(.{1,80}?)\s*$", ln)
        if m: kv[norm(m.group(1))].append((norm(m.group(2)), ln_no))
    conflicts = [{"key": k, "values": [{"value": v, "line": n} for v, n in vals]} for k, vals in kv.items() if len({v for v, _ in vals}) > 1]
    sents = re.split(r"(?<=[.!?])\s+|\n+", text)
    neg = []
    stripped = {}
    for s in sents:
        n = norm(s)
        base = re.sub(r"\b(no|not|nunca|never|n't)\b", "", n); base = re.sub(r"\s+", " ", base).strip()
        has_neg = bool(re.search(r"\b(no|not|nunca|never)\b|n't", n))
        if len(base) > 25: stripped.setdefault(base, set()).add(has_neg)
    for base, flags in stripped.items():
        if flags == {True, False}: neg.append(base[:90])
    L = max(1, len(text)); low = text.lower(); pos = []
    for f in [x.strip().lower() for x in facts if x.strip()]:
        i = low.find(f)
        if i < 0: pos.append({"fact": f, "found": False})
        else:
            r = round(i / L, 2); pos.append({"fact": f, "found": True, "position": r, "risk": "lost-in-middle" if 0.3 <= r <= 0.7 else "ok"})
    toks = round(len(text) / cpt); util = toks / window
    signals = {"distraction_repetition": len(repeats), "clash_key_conflicts": len(conflicts), "clash_negations": len(neg),
               "lost_in_middle_facts": sum(1 for p in pos if p.get("risk") == "lost-in-middle"), "missing_facts": sum(1 for p in pos if not p["found"])}
    sev = "alta" if util > .8 or signals["clash_key_conflicts"] + signals["clash_negations"] > 2 else "media" if any(signals.values()) or util > .5 else "baja"
    mit = []
    if repeats: mit.append("Deduplicar parrafos repetidos.")
    if conflicts or neg: mit.append("Resolver contradicciones: conservar la version vigente y marcar la anterior como obsoleta (o eliminarla).")
    if signals["lost_in_middle_facts"]: mit.append("Reubicar datos criticos al inicio/final o repetirlos en un resumen anclado.")
    if util > .5: mit.append("Compactar o dividir el contexto (ver context-compression / context-optimization).")
    return {"tokens_est": toks, "utilization_pct": round(100 * util, 1), "severity": sev, "signals": signals,
            "repeated_paragraphs": repeats, "key_conflicts": conflicts, "negation_pairs": neg, "fact_positions": pos, "mitigations": mit}

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check"); c.add_argument("file"); c.add_argument("--facts", default="")
    c.add_argument("--window", type=int, default=128000); c.add_argument("--cpt", type=float, default=4.0)
    a = ap.parse_args(argv)
    print(json.dumps(check(open(a.file, encoding="utf-8").read(), a.facts.split(","), a.window, a.cpt), ensure_ascii=False, indent=2)); return 0

if __name__ == "__main__": sys.exit(main())
