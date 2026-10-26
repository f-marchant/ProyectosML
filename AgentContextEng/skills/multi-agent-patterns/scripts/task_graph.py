#!/usr/bin/env python3
"""multi-agent-patterns: analiza un grafo de subtareas para decidir si multiples agentes se justifican.

Uso:
  python task_graph.py plan GRAFO.json [--overhead 1.5]
  python task_graph.py handoff PAQUETE.json          # valida un paquete de traspaso entre agentes
GRAFO.json: {"tasks":[{"id","deps":[],"tokens":int,"context":["tema",...],"agent":"opcional"}]}
Calcula: ciclos, orden topologico, oleadas paralelas, ruta critica (tokens), aislamiento de contexto por solapamiento
y comparativa de costo single-agent vs multi-agente (overhead de coordinacion configurable).
"""
import argparse, json, sys

def plan(g, overhead):
    T = {t["id"]: t for t in g["tasks"]}
    for t in T.values():
        for d in t.get("deps", []):
            if d not in T: return {"error": f"dependencia inexistente: {d} (en {t['id']})"}
    indeg = {i: len(t.get("deps", [])) for i, t in T.items()}; waves = []; done = set()
    while len(done) < len(T):
        ready = sorted(i for i in T if i not in done and all(d in done for d in T[i].get("deps", [])))
        if not ready: return {"error": "ciclo detectado", "pendientes": sorted(set(T) - done)}
        waves.append(ready); done.update(ready)
    best = {}; prev = {}
    for w in waves:
        for i in w:
            ds = T[i].get("deps", []); b = max(ds, key=lambda d: best[d], default=None)
            best[i] = T[i].get("tokens", 0) + (best[b] if b else 0); prev[i] = b
    end = max(best, key=best.get); path = []; c = end
    while c: path.append(c); c = prev[c]
    total = sum(t.get("tokens", 0) for t in T.values())
    single_ctx = total
    ctxs = {i: set(T[i].get("context", [])) for i in T}; allc = set().union(*ctxs.values()) if ctxs else set()
    avg_overlap = 0.0; pairs = [(a, b) for a in T for b in T if a < b]
    if pairs: avg_overlap = sum(len(ctxs[a] & ctxs[b]) / max(1, len(ctxs[a] | ctxs[b])) for a, b in pairs) / len(pairs)
    multi_cost = round(total * overhead); max_par = max(len(w) for w in waves)
    just = []
    if max_par < 2: just.append("No hay paralelismo: un solo agente suficiente.")
    if avg_overlap > 0.5: just.append("Alto solapamiento de contexto: el aislamiento aporta poco y duplicas tokens.")
    if single_ctx > 100000: just.append("El contexto unico seria muy grande: separar por aislamiento de contexto es razonable.")
    if max_par >= 2 and avg_overlap <= 0.5: just.append("Subtareas independientes con contexto distinto: multi-agente razonable.")
    return {"tasks": len(T), "waves": waves, "max_parallel": max_par, "critical_path": list(reversed(path)), "critical_path_tokens": best[end],
            "total_tokens": total, "est_multi_agent_tokens": multi_cost, "overhead_factor": overhead,
            "latency_speedup_vs_sequential": round(total / best[end], 2) if best[end] else None, "context_overlap_avg": round(avg_overlap, 2),
            "distinct_context_topics": len(allc), "assessment": just}

REQ = ["from", "to", "task", "context", "expected_output"]
def handoff(p):
    miss = [k for k in REQ if not p.get(k)]; warn = []
    if p.get("context") and len(json.dumps(p["context"])) > 8000: warn.append("Contexto del traspaso >8000 chars: resumir.")
    if "expected_output" in p and len(str(p["expected_output"])) < 15: warn.append("expected_output demasiado vago.")
    if not p.get("done_criteria"): warn.append("Falta done_criteria (cuando el receptor debe detenerse).")
    if not p.get("constraints"): warn.append("Sin constraints (limites de herramientas, tiempo o alcance).")
    return {"valid": not miss, "missing_fields": miss, "warnings": warn}

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("plan"); p.add_argument("file"); p.add_argument("--overhead", type=float, default=1.5)
    h = sub.add_parser("handoff"); h.add_argument("file"); a = ap.parse_args(argv)
    d = json.load(open(a.file)); print(json.dumps(plan(d, a.overhead) if a.cmd == "plan" else handoff(d), ensure_ascii=False, indent=2)); return 0

if __name__ == "__main__": sys.exit(main())
