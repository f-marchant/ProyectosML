#!/usr/bin/env python3
"""context-optimization: enmascaramiento de observaciones, chequeo de prefijo/cache y presupuesto.

Uso:
  python optimize_context.py mask MENSAJES.json --store store.json [--min-chars 800] [--keep-last 2] > salida.json
  python optimize_context.py restore REF_ID --store store.json
  python optimize_context.py cache-check PROMPTS.json            # lista de strings: prefijo comun y elementos volatiles
  python optimize_context.py budget --window 128000 --alloc "system=10,tools=15,history=40,retrieval=25,reserve=10" --used "system=3000,..."
MENSAJES.json: [{"role":"tool|user|assistant|system","content":"..."}]
"""
import argparse, hashlib, json, os, re, sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR.parent.parent / "_shared"))
from safe_io import atomic_write_json, load_json

def est(t, cpt=4.0): return max(1, round(len(t) / cpt))

def mask(msgs, store_path, min_chars, keep_last):
    store = load_json(store_path, {})
    tool_idx = [i for i, m in enumerate(msgs) if m.get("role") == "tool"]
    protect = set(tool_idx[-keep_last:]) if keep_last else set()
    saved = 0; out = []
    for i, m in enumerate(msgs):
        c = m.get("content", "")
        if m.get("role") == "tool" and i not in protect and len(c) >= min_chars:
            ref = hashlib.sha1(c.encode()).hexdigest()[:8]; store[ref] = c
            first = next((l.strip() for l in c.splitlines() if l.strip()), "")[:100]
            nm = {**m, "content": f"[obs:{ref} omitida ({est(c)} tokens est.). Resumen: {first} ... Recuperable: restore {ref}]"}
            saved += est(c) - est(nm["content"]); out.append(nm)
        else: out.append(m)
    atomic_write_json(store_path, store)
    return out, saved

VOLATILE = [("timestamp", r"\b\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}(?::\d{2})?"), ("fecha", r"\b\d{4}-\d{2}-\d{2}\b"), ("uuid", r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b"),
            ("hora", r"\b\d{1,2}:\d{2}(?::\d{2})?\b"), ("session_id", r"(?i)\b(?:session|request|trace)[_\- ]?id\W+\w+")]

def cache_check(prompts):
    pre = os.path.commonprefix(prompts); k = pre.rfind("\n"); stable = pre[: k + 1] if k > 0 else pre
    vol = []
    for name, rx in VOLATILE:
        for pi, p in enumerate(prompts):
            for m in re.finditer(rx, p):
                if m.start() < len(pre) + 200: vol.append({"type": name, "prompt": pi, "offset": m.start(), "text": m.group(0)})
    first_vol = min((v["offset"] for v in vol), default=None)
    avg = sum(len(p) for p in prompts) / len(prompts)
    return {"prompts": len(prompts), "common_prefix_chars": len(pre), "stable_prefix_tokens_est": est(stable), "avg_prompt_tokens_est": est("x" * int(avg)),
            "reusable_pct": round(100 * len(stable) / avg, 1) if avg else 0, "volatile_items": vol[:20],
            "advice": ("Mover contenido volatil (" + vol[0]["type"] + ") despues del prefijo estable o sustituirlo por un marcador.") if vol and first_vol is not None and first_vol < len(pre) + 50 else "Prefijo estable razonable." if pre else "Sin prefijo comun: reordenar para que instrucciones fijas vayan primero."}

def budget(window, alloc, used):
    a = {k: float(v) for k, v in (x.split("=") for x in alloc.split(","))}
    tot = sum(a.values()); u = {k: int(v) for k, v in (x.split("=") for x in used.split(","))} if used else {}
    rows = []
    for k, pct in a.items():
        cap = round(window * pct / tot); cur = u.get(k, 0)
        rows.append({"category": k, "cap_tokens": cap, "used": cur, "status": "excedido" if cur > cap else "ok", "over_by": max(0, cur - cap)})
    return {"window": window, "alloc_normalized_pct": {k: round(100 * v / tot, 1) for k, v in a.items()}, "categories": rows, "total_used": sum(u.values()), "total_used_pct": round(100 * sum(u.values()) / window, 1)}

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    m = sub.add_parser("mask"); m.add_argument("file"); m.add_argument("--store", required=True); m.add_argument("--min-chars", type=int, default=800); m.add_argument("--keep-last", type=int, default=2)
    r = sub.add_parser("restore"); r.add_argument("ref"); r.add_argument("--store", required=True)
    c = sub.add_parser("cache-check"); c.add_argument("file")
    b = sub.add_parser("budget"); b.add_argument("--window", type=int, required=True); b.add_argument("--alloc", required=True); b.add_argument("--used", default="")
    a = ap.parse_args(argv)
    if a.cmd == "mask":
        out, saved = mask(json.load(open(a.file)), a.store, a.min_chars, a.keep_last)
        print(json.dumps(out, ensure_ascii=False, indent=2)); print(f"# tokens ahorrados (est.): {saved}", file=sys.stderr)
    elif a.cmd == "restore":
        s = json.load(open(a.store))
        if a.ref not in s: print("ref no encontrada", file=sys.stderr); return 1
        print(s[a.ref])
    elif a.cmd == "cache-check": print(json.dumps(cache_check(json.load(open(a.file))), ensure_ascii=False, indent=2))
    else: print(json.dumps(budget(a.window, a.alloc, a.used), ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__": sys.exit(main())
