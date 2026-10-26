#!/usr/bin/env python3
"""filesystem-context: offloading de salidas grandes, plan persistente y descubrimiento bajo demanda.

Uso (directorio de trabajo con --root, por defecto ./.ctx):
  python scratchpad.py offload ARCHIVO_O_- [--name tool_out] [--threshold 2000]   # guarda y devuelve referencia + resumen
  python scratchpad.py read REF [--lines 1:40]      | grep REF PATRON [-C 2]
  python scratchpad.py plan init "paso1" "paso2" ...| plan done N | plan show
  python scratchpad.py index | cleanup [--days 7] [--apply]
Solo biblioteca estandar. Estado en archivos: scratch/*.txt, plan.json, index.json.
"""
import argparse, json, os, re, sys, time, hashlib
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR.parent.parent / "_shared"))
from safe_io import SafeIOError, atomic_write_json, atomic_write_text, load_json

def paths(root):
    os.makedirs(os.path.join(root, "scratch"), exist_ok=True); return os.path.join(root, "scratch"), os.path.join(root, "plan.json"), os.path.join(root, "index.json")

def jl(p, default):
    return load_json(p, default)

def summary(text):
    lines = [l for l in text.splitlines() if l.strip()]
    keys = [l.strip()[:120] for l in lines if re.search(r"(?i)error|fail|warn|exception|total|summary|result", l)][:5]
    return {"lines": len(text.splitlines()), "chars": len(text), "head": [l.strip()[:120] for l in lines[:3]], "tail": [l.strip()[:120] for l in lines[-2:]], "key_lines": keys}

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=".ctx"); sub = ap.add_subparsers(dest="cmd", required=True)
    o = sub.add_parser("offload"); o.add_argument("src"); o.add_argument("--name", default="out"); o.add_argument("--threshold", type=int, default=2000)
    r = sub.add_parser("read"); r.add_argument("ref"); r.add_argument("--lines")
    g = sub.add_parser("grep"); g.add_argument("ref"); g.add_argument("pattern"); g.add_argument("-C", type=int, default=0)
    p = sub.add_parser("plan"); p.add_argument("action", choices=["init", "done", "show"]); p.add_argument("items", nargs="*")
    sub.add_parser("index"); c = sub.add_parser("cleanup"); c.add_argument("--days", type=float, default=7); c.add_argument("--apply", action="store_true")
    a = ap.parse_args(argv); sd, pp, ip = paths(a.root); idx = jl(ip, {})
    if a.cmd == "offload":
        text = sys.stdin.read() if a.src == "-" else open(a.src, encoding="utf-8", errors="replace").read()
        if len(text) < a.threshold: print(json.dumps({"offloaded": False, "reason": f"< {a.threshold} chars", "content": text}, ensure_ascii=False)); return 0
        ref = f"{a.name}_{hashlib.sha1(text.encode()).hexdigest()[:8]}"; atomic_write_text(os.path.join(sd, ref + ".txt"), text)
        idx[ref] = {"created": time.time(), "chars": len(text)}; atomic_write_json(ip, idx)
        print(json.dumps({"offloaded": True, "ref": ref, "path": os.path.join(sd, ref + ".txt"), "summary": summary(text)}, ensure_ascii=False, indent=2))
    elif a.cmd in ("read", "grep"):
        f = os.path.join(sd, a.ref + ".txt")
        if not os.path.exists(f): print("ref no encontrada", file=sys.stderr); return 1
        L = open(f, encoding="utf-8").read().splitlines()
        if a.cmd == "read":
            s, e = (a.lines.split(":") + [""])[:2] if a.lines else ("1", str(len(L)))
            s = int(s or 1); e = int(e or len(L)); print("\n".join(f"{i}: {L[i-1]}" for i in range(max(1, s), min(len(L), e) + 1)))
        else:
            try:
                rx = re.compile(a.pattern)
            except re.error as exc:
                print(f"error: patron invalido: {exc}", file=sys.stderr); return 2
            shown = set()
            for i, l in enumerate(L):
                if rx.search(l): shown.update(range(max(0, i - a.C), min(len(L), i + a.C + 1)))
            print("\n".join(f"{i+1}: {L[i]}" for i in sorted(shown)) or "sin coincidencias")
    elif a.cmd == "plan":
        plan = jl(pp, {"steps": []})
        if a.action == "init": plan = {"steps": [{"n": i + 1, "text": t, "done": False} for i, t in enumerate(a.items)]}
        elif a.action == "done":
            n = int(a.items[0]); [s.update(done=True) for s in plan["steps"] if s["n"] == n]
        atomic_write_json(pp, plan)
        print("\n".join(f"[{'x' if s['done'] else ' '}] {s['n']}. {s['text']}" for s in plan["steps"]))
        nxt = next((s for s in plan["steps"] if not s["done"]), None); print("Siguiente:", nxt["text"] if nxt else "completado")
    elif a.cmd == "index":
        print(json.dumps({k: {"chars": v["chars"], "age_h": round((time.time() - v["created"]) / 3600, 1)} for k, v in idx.items()}, indent=2))
    else:
        old = [k for k, v in idx.items() if time.time() - v["created"] > a.days * 86400]
        if a.apply:
            for k in old: os.remove(os.path.join(sd, k + ".txt")); idx.pop(k)
            atomic_write_json(ip, idx)
        print(json.dumps({"expired": old, "deleted": a.apply}))
    return 0

if __name__ == "__main__": sys.exit(main())
