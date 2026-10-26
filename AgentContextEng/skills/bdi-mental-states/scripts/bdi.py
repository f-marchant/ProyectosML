#!/usr/bin/env python3
"""bdi-mental-states: transforma hechos (triples) en estados mentales BDI mediante reglas, valida el modelo y exporta Turtle.

Uso:
  python bdi.py transform HECHOS.tsv REGLAS.json [--agent ex:agent1] [--format turtle|json]
  python bdi.py check MODELO.json
HECHOS.tsv: una triple por linea: sujeto<TAB>predicado<TAB>objeto  (nombres prefijados, p.ej. ex:order42  ex:status  ex:delayed)
REGLAS.json: {"desires":[{"id","when":{"p":"ex:status","o":"ex:delayed"},"goal":"ex:notifyCustomer"}],
              "intentions":[{"desire":"id","requires":[{"p":"ex:hasContact","o":"*"}],"plan":["tarea1","tarea2"]}]}
Cadena formal: Belief(refersTo WorldState) -motivates-> Desire <-fulfils- Intention(isSupportedBy Belief, specifies Plan).
Una intencion solo se crea si TODAS sus precondiciones tienen creencias de apoyo (viabilidad deliberativa).
"""
import argparse, json, re, sys

def slug(*p): return re.sub(r"[^A-Za-z0-9]+", "_", "_".join(p)).strip("_")

def match(rule, t): return (rule.get("p") in (None, "*", t[1])) and (rule.get("o") in (None, "*", t[2])) and (rule.get("s") in (None, "*", t[0]))

def validate_triples(triples):
    if any(len(t) != 3 or any(not part for part in t) for t in triples):
        raise ValueError("cada hecho debe tener sujeto, predicado y objeto separados por TAB")

def turtle_literal(value):
    return str(value).replace("\\", "\\\\").replace('"', '\\"').replace("\r", "\\r").replace("\n", "\\n")

def transform(triples, rules, agent):
    M = {"agent": agent, "world_states": [], "beliefs": [], "desires": [], "intentions": [], "plans": []}
    for i, t in enumerate(triples):
        ws = f"ex:ws_{i}"; M["world_states"].append({"id": ws, "triple": list(t)})
        M["beliefs"].append({"id": f"ex:belief_{slug(*t)}", "refersTo": ws, "triple": list(t), "justifiedBy": f"ex:src_{i}"})
    for d in rules.get("desires", []):
        sup = [b for b in M["beliefs"] if match(d["when"], tuple(b["triple"]))]
        if sup: M["desires"].append({"id": f"ex:desire_{d['id']}", "rule": d["id"], "goal": d["goal"], "isMotivatedBy": [b["id"] for b in sup]})
    for it in rules.get("intentions", []):
        des = next((x for x in M["desires"] if x["rule"] == it["desire"]), None)
        if not des: continue
        sup, ok = [], True
        for req in it.get("requires", []):
            hit = [b["id"] for b in M["beliefs"] if match(req, tuple(b["triple"]))]
            if not hit: ok = False; break
            sup += hit
        if ok:
            plan = f"ex:plan_{it['desire']}"; M["plans"].append({"id": plan, "addresses": des["goal"], "tasks": it.get("plan", [])})
            M["intentions"].append({"id": f"ex:intention_{it['desire']}", "fulfils": des["id"], "isSupportedBy": sorted(set(sup)) or des["isMotivatedBy"], "specifies": plan})
    return M

def check(M):
    err = []; B = {b["id"] for b in M["beliefs"]}; D = {d["id"]: d for d in M["desires"]}; W = {w["id"] for w in M["world_states"]}; P = {p["id"] for p in M["plans"]}
    for b in M["beliefs"]:
        if b.get("refersTo") not in W: err.append(f"Belief {b['id']} no refiere a un WorldState.")
    for d in M["desires"]:
        if not d.get("isMotivatedBy") or any(x not in B for x in d["isMotivatedBy"]): err.append(f"Desire {d['id']} sin creencia motivadora valida.")
    for i in M["intentions"]:
        if i["fulfils"] not in D: err.append(f"Intention {i['id']} no cumple ningun Desire.")
        if not i.get("isSupportedBy") or any(x not in B for x in i["isSupportedBy"]): err.append(f"Intention {i['id']} sin creencias de apoyo.")
        if i.get("specifies") not in P: err.append(f"Intention {i['id']} sin Plan.")
    orphan = [d for d in D if not any(i["fulfils"] == d for i in M["intentions"])]
    return {"valid": not err, "errors": err, "counts": {k: len(M[k]) for k in ("world_states", "beliefs", "desires", "intentions", "plans")}, "desires_without_intention": orphan}

def turtle(M):
    L = ["@prefix bdi: <http://example.org/bdi#> .", "@prefix ex: <http://example.org/ex#> .", "@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .", "@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .", ""]
    for w in M["world_states"]: L.append(f"{w['id']} a bdi:WorldState ; rdfs:comment \"{turtle_literal(' '.join(w['triple']))}\" .")
    for b in M["beliefs"]: L.append(f"{b['id']} a bdi:Belief ; bdi:refersTo {b['refersTo']} ; bdi:isJustifiedBy {b['justifiedBy']} .")
    for d in M["desires"]: L.append(f"{d['id']} a bdi:Desire ; bdi:isMotivatedBy {', '.join(d['isMotivatedBy'])} .")
    for i in M["intentions"]: L.append(f"{i['id']} a bdi:Intention ; bdi:fulfils {i['fulfils']} ; bdi:isSupportedBy {', '.join(i['isSupportedBy'])} ; bdi:specifies {i['specifies']} .")
    for p in M["plans"]: L.append(f"{p['id']} a bdi:Plan ; bdi:addresses {p['addresses']} ; rdfs:comment \"{turtle_literal(' -> '.join(p['tasks']))}\" .")
    return "\n".join(L)

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    t = sub.add_parser("transform"); t.add_argument("facts"); t.add_argument("rules"); t.add_argument("--agent", default="ex:agent1"); t.add_argument("--format", choices=["turtle", "json"], default="turtle")
    c = sub.add_parser("check"); c.add_argument("model"); a = ap.parse_args(argv)
    try:
        if a.cmd == "transform":
            tr = [tuple(l.rstrip("\n").split("\t")[:3]) for l in open(a.facts, encoding="utf-8") if l.strip() and not l.startswith("#")]
            validate_triples(tr)
            rules = json.load(open(a.rules, encoding="utf-8"))
            if not isinstance(rules, dict):
                raise ValueError("las reglas deben ser un objeto JSON")
            M = transform(tr, rules, a.agent); print(turtle(M) if a.format == "turtle" else json.dumps(M, ensure_ascii=False, indent=2))
        else:
            out = check(json.load(open(a.model, encoding="utf-8"))); print(json.dumps(out, ensure_ascii=False, indent=2)); return 0 if out["valid"] else 1
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError, KeyError) as exc:
        print(f"error: {exc}", file=sys.stderr); return 2
    return 0

if __name__ == "__main__": sys.exit(main())
