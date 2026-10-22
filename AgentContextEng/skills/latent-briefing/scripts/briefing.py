#!/usr/bin/env python3
"""latent-briefing: aproximacion A NIVEL DE TEXTO del briefing orquestador->worker, y modelo de costo.

El metodo original opera sobre el KV cache del modelo worker (requiere runtime controlable). Aqui se implementa su analogo textual:
segmentos de la trayectoria puntuados contra la tarea del worker (BM25), mascara comun con umbral robusto (mediana + k*MAD) y orden preservado.
Uso:
  python briefing.py compact TRAYECTORIA.txt --task "tarea del worker" [--k 0.5] [--min-keep 3] [--max-keep-ratio 0.5]
  python briefing.py cost --trajectory-tokens 40000 --workers 6 --doc-tokens 3000 [--summary-tokens 2000] [--keep-ratio 0.25] [--calls-per-worker 3]
"""
import argparse, json, math, re, statistics, sys

def tok(t): return re.findall(r"\w+", t.lower())

def segments(text):
    segs = [s.strip() for s in re.split(r"\n\s*\n|\n(?=\[|Turn |Paso |Step )", text) if s.strip()]
    return segs if len(segs) > 2 else [l for l in text.splitlines() if l.strip()]

def bm25_scores(segs, q, k1=1.5, b=0.75):
    docs = [tok(s) for s in segs]; N = len(docs); avg = sum(map(len, docs)) / N or 1; df = {}
    for d in docs:
        for w in set(d): df[w] = df.get(w, 0) + 1
    qs = set(tok(q)); out = []
    for d in docs:
        s = 0.0
        for w in qs:
            if w in df:
                f = d.count(w); s += math.log(1 + (N - df[w] + .5) / (df[w] + .5)) * f * (k1 + 1) / (f + k1 * (1 - b + b * len(d) / avg))
        out.append(s)
    return out

def compact(text, task, k, min_keep, max_ratio):
    segs = segments(text); sc = bm25_scores(segs, task); med = statistics.median(sc)
    mad = statistics.median([abs(x - med) for x in sc]) or (max(sc) / 10 if max(sc) else 1)
    thr = med + k * mad; keep = {i for i, s in enumerate(sc) if s >= thr and s > 0}
    order = sorted(range(len(segs)), key=lambda i: -sc[i])
    for i in order:
        if len(keep) >= min_keep: break
        keep.add(i)
    cap = max(min_keep, int(len(segs) * max_ratio))
    if len(keep) > cap: keep = set(sorted(keep, key=lambda i: -sc[i])[:cap])
    for i in list(keep):
        if i > 0 and segs[i].lower().startswith(("resultado", "result", "->")): keep.add(i - 1)
    kept = [segs[i] for i in sorted(keep)]; out = "\n\n".join(kept)
    return {"segments_total": len(segs), "segments_kept": len(kept), "threshold": round(thr, 3), "chars_before": len(text), "chars_after": len(out),
            "reduction_pct": round(100 * (1 - len(out) / max(len(text), 1)), 1), "briefing": out}

def cost(a):
    n, T, D, S, r, c = a.workers, a.trajectory_tokens, a.doc_tokens, a.summary_tokens, a.keep_ratio, a.calls_per_worker
    rows = {"full_trajectory": n * c * (T + D), "summary_handoff": n * c * (S + D) + T * 0.1 * n,
            "retrieval_only": n * c * (D + 0.05 * T), "text_briefing": n * c * (T * r + D)}
    base = rows["full_trajectory"]
    return {"inputs": vars(a) | {"cmd": None}, "worker_input_tokens": {k: round(v) for k, v in rows.items()},
            "vs_full_pct": {k: round(100 * v / base, 1) for k, v in rows.items()},
            "note": "Modelo de costo de ENTRADA de workers; la variante latente real ahorra ademas calculo de prefill, que este modelo no captura."}

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("compact"); c.add_argument("file"); c.add_argument("--task", required=True); c.add_argument("--k", type=float, default=0.5); c.add_argument("--min-keep", type=int, default=3); c.add_argument("--max-keep-ratio", type=float, default=0.5)
    s = sub.add_parser("cost"); s.add_argument("--trajectory-tokens", type=int, required=True); s.add_argument("--workers", type=int, required=True); s.add_argument("--doc-tokens", type=int, default=0)
    s.add_argument("--summary-tokens", type=int, default=2000); s.add_argument("--keep-ratio", type=float, default=0.25); s.add_argument("--calls-per-worker", type=int, default=1)
    a = ap.parse_args(argv)
    out = compact(open(a.file, encoding="utf-8").read(), a.task, a.k, a.min_keep, a.max_keep_ratio) if a.cmd == "compact" else cost(a)
    print(json.dumps(out, ensure_ascii=False, indent=2)); return 0

if __name__ == "__main__": sys.exit(main())
