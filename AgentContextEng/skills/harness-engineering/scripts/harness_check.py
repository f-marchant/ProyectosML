#!/usr/bin/env python3
"""harness-engineering: validacion de configuracion de harness y ledger de experimentos append-only con cadena de hashes.

Uso:
  python harness_check.py validate HARNESS.json
  python harness_check.py ledger append LEDGER.jsonl --hypothesis "..." --metric 0.71 [--status kept|discarded] [--note "..."]
  python harness_check.py ledger verify LEDGER.jsonl
  python harness_check.py ledger novelty LEDGER.jsonl "nueva hipotesis" [--threshold 0.6]
  python harness_check.py ledger decide LEDGER.jsonl --metric 0.74 [--higher-is-better] [--min-delta 0.01]
HARNESS.json: {"metric":{"name","locked":true,"direction":"max|min"},"locked_surfaces":[...],"editable_surfaces":[...],
  "log":{"path","append_only":true},"rollback":{"enabled":true,"trigger":"..."},"novelty_gate":true,
  "approval_required_for":["push","merge","delete","deploy","spend"],"actions":["read","edit","push",...],"budget":{"max_iterations":n}}
"""
import argparse, hashlib, json, os, re, sys, time
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR.parent.parent / "_shared"))
from safe_io import FileLock, SafeIOError, load_json

IRREV = {"push", "merge", "delete", "deploy", "spend", "send_email", "publish", "force_push", "drop"}

def validate(h):
    err, warn = [], []
    m = h.get("metric", {})
    if not m.get("name"): err.append("Falta metric.name.")
    if m.get("locked") is not True: err.append("La metrica debe estar bloqueada (metric.locked=true): el optimizador no puede editar su propio evaluador.")
    if m.get("direction") not in ("max", "min"): err.append("metric.direction debe ser 'max' o 'min'.")
    L, E = set(h.get("locked_surfaces", [])), set(h.get("editable_surfaces", []))
    if not L: warn.append("Sin locked_surfaces declaradas.")
    if not E: err.append("Sin editable_surfaces: el agente no tiene nada que modificar.")
    both = L & E
    if both: err.append(f"Superficies a la vez bloqueadas y editables: {sorted(both)}.")
    for e in E:
        for l in L:
            if e != l and (e.startswith(l.rstrip('/') + '/') or l.startswith(e.rstrip('/') + '/')): err.append(f"Solapamiento de rutas editable '{e}' y bloqueada '{l}'.")
    lg = h.get("log", {})
    if not lg.get("path"): err.append("Falta log.path (registro durable).")
    if lg.get("append_only") is not True: warn.append("El log deberia ser append_only.")
    r = h.get("rollback", {})
    if not r.get("enabled"): err.append("Rollback deshabilitado.")
    elif not r.get("trigger"): warn.append("rollback.trigger no definido.")
    if not h.get("novelty_gate"): warn.append("Sin novelty_gate: riesgo de repetir experimentos.")
    appr = set(h.get("approval_required_for", [])); acts = set(h.get("actions", []))
    unguarded = sorted((acts & IRREV) - appr)
    if unguarded: err.append(f"Acciones irreversibles sin aprobacion humana: {unguarded}.")
    if not h.get("budget", {}).get("max_iterations"): warn.append("Sin budget.max_iterations: bucle sin tope.")
    return {"valid": not err, "errors": err, "warnings": warn}

def last_hash(p):
    if not os.path.exists(p): return "0" * 64
    try:
        ls = [l for l in open(p, encoding="utf-8") if l.strip()]
        return json.loads(ls[-1])["hash"] if ls else "0" * 64
    except (OSError, json.JSONDecodeError, KeyError) as exc:
        raise SafeIOError(f"ledger invalido '{p}': {exc}") from exc

def digest(rec): return hashlib.sha256(json.dumps({k: v for k, v in rec.items() if k != "hash"}, sort_keys=True, ensure_ascii=False).encode()).hexdigest()

def read(p):
    if not os.path.exists(p):
        return []
    try:
        return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]
    except (OSError, json.JSONDecodeError) as exc:
        raise SafeIOError(f"ledger invalido '{p}': {exc}") from exc

def tok(t): return set(re.findall(r"\w{3,}", t.lower()))

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True); v = sub.add_parser("validate"); v.add_argument("file")
    l = sub.add_parser("ledger"); l.add_argument("action", choices=["append", "verify", "novelty", "decide"]); l.add_argument("file"); l.add_argument("text", nargs="?")
    l.add_argument("--hypothesis"); l.add_argument("--metric", type=float); l.add_argument("--status", default="kept"); l.add_argument("--note", default="")
    l.add_argument("--threshold", type=float, default=0.6); l.add_argument("--higher-is-better", action="store_true"); l.add_argument("--min-delta", type=float, default=0.0)
    a = ap.parse_args(argv)
    if a.cmd == "validate":
        try:
            print(json.dumps(validate(load_json(a.file)), ensure_ascii=False, indent=2)); return 0
        except SafeIOError as exc:
            print(f"error: {exc}", file=sys.stderr); return 2
    if a.action == "append":
        if not a.hypothesis or a.metric is None or a.status not in ("kept", "discarded"):
            print("error: append requiere hypothesis, metric y status kept|discarded", file=sys.stderr); return 2
        try:
            with FileLock(a.file):
                rec = {"ts": time.strftime("%Y-%m-%dT%H:%M:%S"), "n": len(read(a.file)) + 1, "hypothesis": a.hypothesis, "metric": a.metric, "status": a.status, "note": a.note, "prev": last_hash(a.file)}
                rec["hash"] = digest(rec)
                with open(a.file, "a", encoding="utf-8") as handle:
                    handle.write(json.dumps(rec, ensure_ascii=False) + "\n")
                    handle.flush()
                    os.fsync(handle.fileno())
            print(json.dumps({"appended": rec["n"], "hash": rec["hash"][:12]}))
        except (OSError, SafeIOError) as exc:
            print(f"error: {exc}", file=sys.stderr); return 2
    elif a.action == "verify":
        prev = "0" * 64; bad = []
        for r in read(a.file):
            if r["prev"] != prev or digest(r) != r["hash"]: bad.append(r["n"])
            prev = r["hash"]
        print(json.dumps({"entries": len(read(a.file)), "intact": not bad, "tampered_entries": bad})); return 1 if bad else 0
    elif a.action == "novelty":
        t = tok(a.text or ""); hits = []
        for r in read(a.file):
            s = tok(r.get("hypothesis") or ""); j = len(t & s) / len(t | s) if t | s else 0
            if j >= a.threshold: hits.append({"n": r["n"], "similarity": round(j, 2), "status": r["status"], "hypothesis": r["hypothesis"]})
        print(json.dumps({"novel": not hits, "similar_previous": hits}, ensure_ascii=False, indent=2))
    else:
        kept = [r["metric"] for r in read(a.file) if r["status"] == "kept" and r["metric"] is not None]
        if not kept: print(json.dumps({"decision": "keep", "reason": "sin linea base previa"})); return 0
        best = max(kept) if a.higher_is_better else min(kept); d = (a.metric - best) if a.higher_is_better else (best - a.metric)
        print(json.dumps({"baseline_best": best, "candidate": a.metric, "improvement": round(d, 6), "decision": "keep" if d > a.min_delta else "discard/rollback"}))
    return 0

if __name__ == "__main__": sys.exit(main())
