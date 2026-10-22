#!/usr/bin/env python3
"""self-managed-context: protocolo de archivo-espejo de contexto editable (segun references/harness-protocol.md).

Uso:
  python ctxfile.py render MENSAJES.json [--protect 2] > contexto.md        # prefijo protegido NO se escribe
  python ctxfile.py apply MENSAJES.json contexto_editado.md [--protect 2] [--gate fit|shrink] [--budget 28000] [--reserve 2048] [--out nuevos.json]
  python ctxfile.py nudge --used 15000 --budget 28000 [--reserve 2048] [--last-outputs 800,5000,300]
MENSAJES.json: [{"role":"system|user|assistant|tool","content":"..."}]
apply: parse-back (re-ancla prefijo; roles no-assistant -> user; elimina turnos vacios; fusiona consecutivos), compuerta de edicion,
recibo, lectura de contexto y costo de cache (tokens invalidados desde el primer cambio). Tokens = estimacion chars/4.
"""
import argparse, json, re, sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR.parent.parent / "_shared"))
from safe_io import atomic_write_json

HDR = re.compile(r"(?m)^\[\[CTX_TURN \d+ role=(\w+)\]\]\n?")
est = lambda t: max(0, round(len(t) / 4))

def render(msgs, protect):
    out = []
    for i, m in enumerate(msgs[protect:], 1): out.append(f"[[CTX_TURN {i} role={m['role']}]]\n{m['content']}\n")
    return "\n".join(out)

def parse_back(text, msgs, protect):
    pre = list(msgs[:protect]); parts = HDR.split(text); turns = []
    if parts[0].strip(): turns.append(("user", parts[0].strip()))
    for j in range(1, len(parts), 2): turns.append((parts[j], parts[j + 1].strip()))
    norm = [("assistant" if r == "assistant" else "user", b) for r, b in turns if b]
    merged = []
    for r, b in norm:
        if merged and merged[-1]["role"] == r: merged[-1]["content"] += "\n\n" + b
        else: merged.append({"role": r, "content": b})
    return pre + merged

def total(ms): return sum(est(m["content"]) for m in ms)

def first_change(old, new):
    for i, (a, b) in enumerate(zip(old, new)):
        if a != b: return i
    return min(len(old), len(new)) if len(old) != len(new) else None

def apply(msgs, edited, protect, gate, budget, reserve):
    base = parse_back(render(msgs, protect), msgs, protect); new = parse_back(edited, msgs, protect)
    tb, ta = total(base), total(new); limit = (budget - reserve) if budget else None
    changed = [m["content"] for m in base] != [m["content"] for m in new] or [m["role"] for m in base] != [m["role"] for m in new]
    if not changed: return {"applied": False, "receipt": "Sin cambios (diferencias de espacios no cuentan).", "messages": msgs}
    grew = ta > tb
    if grew and (gate == "shrink" or (gate == "fit" and (limit is None or ta > limit))):
        why = "gate=shrink: todo crecimiento se rechaza" if gate == "shrink" else ("sin presupuesto configurado: crecimiento rechazado" if limit is None else "el resultado excede el presupuesto")
        return {"applied": False, "receipt": f"RECHAZADO ({why}). Tokens {tb} -> {ta}. Contexto sin cambios.", "messages": msgs}
    idx = first_change(base, new); inval = sum(est(m["content"]) for m in base[idx:]) if idx is not None else 0
    tail = sum(est(m["content"]) for m in base[idx + 1:]) if idx is not None else 0
    rec = f"APLICADO. Tokens {tb} -> {ta}, turnos {len(base)-protect} -> {len(new)-protect}."
    if grew: rec += " El contexto CRECIO: probablemente se duplico en vez de reemplazar."
    if limit is not None: rec += f" [context: ~{ta}/{limit} tokens]" + (" OVER: compacta ahora o termina la sesion." if ta > limit else "")
    return {"applied": True, "tokens_before": tb, "tokens_after": ta, "grew": grew, "first_changed_turn": None if idx is None else idx - protect + 1, "cache_tokens_invalidated_est": inval,
            "cache_note": "Un cambio temprano bajo una cola larga invalida todo lo posterior en el prefix cache." if tail > 2 * max(1, tb - ta) and tb > ta else "", "receipt": rec, "messages": new}

def nudge(used, budget, reserve, outs):
    limit = budget - reserve; fill = used / limit; band = min(max(0.1 * limit, 2 * max(outs, default=0)), 0.5 * limit); remaining = limit - used
    if remaining <= band: lvl, msg = "urgente", "Compacta ESTA vuelta y no hagas nada mas; cruzar el limite da una ultima vuelta."
    elif fill > .75: lvl, msg = "alto", "Cerca del limite: compacta tramos resueltos sin vaciar; incluye el contrato de notas."
    elif fill > .5: lvl, msg = "medio", "Termina la unidad de trabajo en curso y ordena una vez."
    elif fill > .25: lvl, msg = "info-25", "Solo informativo: mantener registro de consultas ya probadas."
    else: lvl, msg = "ninguno", "Sin accion."
    return {"limit": limit, "used": used, "fill_pct": round(100 * fill, 1), "urgent_band_tokens": round(band), "tokens_to_limit": remaining, "level": lvl, "message": msg,
            "note_contract": "Al reescribir: copiar hechos, candidatos descartados con motivo y 'no reintentar', comandos ya probados, valores verificados/no verificados y siguiente paso." if lvl in ("medio", "alto", "urgente") else None}

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("render"); r.add_argument("msgs"); r.add_argument("--protect", type=int, default=2)
    p = sub.add_parser("apply"); p.add_argument("msgs"); p.add_argument("edited"); p.add_argument("--protect", type=int, default=2); p.add_argument("--gate", default="fit", choices=["fit", "shrink"]); p.add_argument("--budget", type=int); p.add_argument("--reserve", type=int, default=2048); p.add_argument("--out")
    n = sub.add_parser("nudge"); n.add_argument("--used", type=int, required=True); n.add_argument("--budget", type=int, required=True); n.add_argument("--reserve", type=int, default=2048); n.add_argument("--last-outputs", default="")
    a = ap.parse_args(argv)
    if a.cmd == "render": print(render(json.load(open(a.msgs)), a.protect))
    elif a.cmd == "apply":
        res = apply(json.load(open(a.msgs)), open(a.edited, encoding="utf-8").read(), a.protect, a.gate, a.budget, a.reserve)
        if a.out and res["applied"]: atomic_write_json(a.out, res["messages"])
        res.pop("messages"); print(json.dumps(res, ensure_ascii=False, indent=2))
    else: print(json.dumps(nudge(a.used, a.budget, a.reserve, [int(x) for x in a.last_outputs.split(",") if x]), ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__": sys.exit(main())
