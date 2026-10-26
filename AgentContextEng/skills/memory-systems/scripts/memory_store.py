#!/usr/bin/env python3
"""memory-systems: memoria persistente en un archivo JSON con busqueda BM25 y grafo de entidades con validez temporal.

Uso:
  python memory_store.py --store mem.json add "Alice trabaja en Acme" [--tags a,b] [--entity Alice]
  python memory_store.py --store mem.json search "donde trabaja Alice" [-k 5]
  python memory_store.py --store mem.json link Alice works_at Acme --from 2024-01-01 [--until 2025-06-30]
  python memory_store.py --store mem.json query Alice [--as-of 2025-01-01]
  python memory_store.py --store mem.json invalidate FACT_ID | consolidate [--threshold 0.85] | stats | export
Solo biblioteca estandar. Recuperacion lexica (BM25), no embeddings. El archivo es el unico estado.
"""
import argparse, json, math, os, re, sys, hashlib
from datetime import date
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR.parent.parent / "_shared"))
from safe_io import FileLock, SafeIOError, atomic_write_json, load_json

def tok(t): return re.findall(r"\w+", t.lower())

def load(p):
    data = load_json(p, {"memories": [], "edges": []})
    if not isinstance(data, dict) or not isinstance(data.get("memories"), list) or not isinstance(data.get("edges"), list):
        raise SafeIOError("el store debe contener listas memories y edges")
    return data

def save(p, d):
    with FileLock(p):
        atomic_write_json(p, d)

def mid(text): return hashlib.sha1(text.encode()).hexdigest()[:8]

def bm25(mems, q, k1=1.5, b=0.75):
    docs = [tok(m["text"]) for m in mems]; N = len(docs) or 1; avg = (sum(map(len, docs)) / N) or 1
    df = {}
    for d in docs:
        for w in set(d): df[w] = df.get(w, 0) + 1
    out = []
    for m, d in zip(mems, docs):
        s = 0.0
        for w in set(tok(q)):
            if w in df:
                f = d.count(w); idf = math.log(1 + (N - df[w] + .5) / (df[w] + .5))
                s += idf * f * (k1 + 1) / (f + k1 * (1 - b + b * len(d) / avg))
        out.append((s, m))
    return sorted([x for x in out if x[0] > 0 and not x[1].get("invalid")], key=lambda x: -x[0])

def jacc(a, b):
    a, b = set(tok(a)), set(tok(b)); return len(a & b) / len(a | b) if a | b else 0

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--store", default="memory.json"); sub = ap.add_subparsers(dest="cmd", required=True)
    a_ = sub.add_parser("add"); a_.add_argument("text"); a_.add_argument("--tags", default=""); a_.add_argument("--entity", default="")
    s_ = sub.add_parser("search"); s_.add_argument("query"); s_.add_argument("-k", type=int, default=5)
    l_ = sub.add_parser("link"); l_.add_argument("src"); l_.add_argument("rel"); l_.add_argument("dst"); l_.add_argument("--from", dest="vfrom", default=str(date.today())); l_.add_argument("--until", default=None)
    q_ = sub.add_parser("query"); q_.add_argument("entity"); q_.add_argument("--as-of", default=str(date.today()))
    i_ = sub.add_parser("invalidate"); i_.add_argument("id")
    c_ = sub.add_parser("consolidate"); c_.add_argument("--threshold", type=float, default=0.85); c_.add_argument("--dry-run", action="store_true")
    sub.add_parser("stats"); sub.add_parser("export")
    a = ap.parse_args(argv)
    if a.cmd == "consolidate" and not 0 <= a.threshold <= 1:
        print("error: threshold debe estar entre 0 y 1", file=sys.stderr); return 2
    try:
        with FileLock(a.store):
            d = load(a.store)
        if a.cmd == "add":
            m = {"id": mid(a.text), "text": a.text, "tags": [t for t in a.tags.split(",") if t], "entity": a.entity, "created": str(date.today())}
            if any(x["id"] == m["id"] for x in d["memories"]): print(json.dumps({"status": "duplicado", "id": m["id"]})); return 0
            d["memories"].append(m); save(a.store, d); print(json.dumps({"status": "ok", "id": m["id"]}))
        elif a.cmd == "search":
            if a.k < 1: print("error: k debe ser positivo", file=sys.stderr); return 2
            print(json.dumps([{"score": round(s, 3), **m} for s, m in bm25(d["memories"], a.query)[: a.k]], ensure_ascii=False, indent=2))
        elif a.cmd == "link":
            d["edges"].append({"src": a.src, "rel": a.rel, "dst": a.dst, "from": a.vfrom, "until": a.until}); save(a.store, d); print(json.dumps({"status": "ok", "edges": len(d["edges"])}))
        elif a.cmd == "query":
            ent = a.entity.lower(); act = [e for e in d["edges"] if ent in (e["src"].lower(), e["dst"].lower()) and e["from"] <= a.as_of and (e["until"] is None or a.as_of <= e["until"])]
            mems = [m for m in d["memories"] if m.get("entity", "").lower() == ent and not m.get("invalid")]
            print(json.dumps({"entity": a.entity, "as_of": a.as_of, "relations": act, "memories": mems}, ensure_ascii=False, indent=2))
        elif a.cmd == "invalidate":
            hit = [m for m in d["memories"] if m["id"] == a.id]
            if not hit: print("id no encontrado", file=sys.stderr); return 1
            hit[0]["invalid"] = True; hit[0]["invalidated"] = str(date.today()); save(a.store, d); print(json.dumps({"status": "invalidado", "id": a.id}))
        elif a.cmd == "consolidate":
            keep, dropped = [], []
            for m in d["memories"]:
                dup = next((k for k in keep if jacc(k["text"], m["text"]) >= a.threshold), None)
                (dropped.append({"dropped": m["id"], "kept": dup["id"]}) if dup else keep.append(m))
            if not a.dry_run:
                d["memories"] = keep; save(a.store, d)
            print(json.dumps({"merged": dropped, "remaining": len(keep), "dry_run": a.dry_run}, indent=2))
        elif a.cmd == "stats":
            print(json.dumps({"memories": len(d["memories"]), "invalid": sum(bool(m.get("invalid")) for m in d["memories"]), "edges": len(d["edges"]),
                              "open_edges": sum(e["until"] is None for e in d["edges"])}, indent=2))
        else: print(json.dumps(d, ensure_ascii=False, indent=2))
        return 0
    except (OSError, SafeIOError, KeyError, TypeError) as exc:
        print(f"error: {exc}", file=sys.stderr); return 2

if __name__ == "__main__": sys.exit(main())
