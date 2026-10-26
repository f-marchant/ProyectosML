#!/usr/bin/env python3
"""tool-design: lint de definiciones de herramientas para agentes.

Uso:
  python tool_lint.py lint TOOLS.json [--overlap 0.5]
  python tool_lint.py describe SPEC.json        # genera descripcion estructurada (que hace / cuando usar / retorna / errores)
TOOLS.json: lista de herramientas estilo OpenAI/Anthropic/MCP: {"name","description","parameters"|"input_schema"|"inputSchema":{properties,required}}
SPEC.json: {"name","purpose","use_when":[],"avoid_when":[],"returns","params":{"p":"desc"},"errors":{"CODIGO":"como corregir"}}
"""
import argparse, json, re, sys

def schema(t): return t.get("parameters") or t.get("input_schema") or t.get("inputSchema") or t.get("function", {}).get("parameters") or {}

def toks(s): return set(w for w in re.findall(r"[a-záéíóúñ]{4,}", s.lower()))

def lint(tools, ov):
    issues = []; names = []
    for t in tools:
        f = t.get("function", t); n = f.get("name", "?"); d = f.get("description", ""); sc = schema(f); props = sc.get("properties", {}); names.append(n)
        def add(sev, msg): issues.append({"tool": n, "severity": sev, "issue": msg})
        if not re.match(r"^[a-z][a-z0-9]*(?:[_\-][a-z0-9]+)*$", n): add("media", "Nombre no sigue snake_case/kebab-case consistente.")
        if len(d) < 60: add("alta", f"Descripcion muy corta ({len(d)} chars): debe indicar que hace, cuando usarla y que retorna.")
        if not re.search(r"(?i)\b(use|usa|usar|when|cuando|si el|if)\b", d): add("media", "No indica CUANDO usar la herramienta.")
        if not re.search(r"(?i)\b(return|retorna|devuelve|returns|output|salida)\b", d): add("media", "No indica QUE retorna.")
        if len(d) > 1500: add("baja", "Descripcion muy larga (>1500): consume contexto en cada llamada.")
        for p, s in props.items():
            if not s.get("description"): add("media", f"Parametro '{p}' sin descripcion.")
            if s.get("type") == "string" and re.search(r"(?i)(format|type|mode|status|order|sort|level)$", p) and "enum" not in s: add("baja", f"Parametro '{p}' podria usar enum.")
        for r in sc.get("required", []):
            if r not in props: add("alta", f"required '{r}' no existe en properties.")
        if len(props) > 8: add("media", f"{len(props)} parametros: considerar dividir o simplificar.")
        if not props and sc: add("baja", "Esquema sin properties.")
    if len(set(names)) != len(names): issues.append({"tool": "*", "severity": "alta", "issue": "Nombres duplicados."})
    pre = [n.split("_")[0] for n in names]
    if len(set(pre)) == len(pre) and len(names) > 4: issues.append({"tool": "*", "severity": "baja", "issue": "Sin prefijo comun/namespace en un catalogo de >4 herramientas."})
    sims = []
    for i, a in enumerate(tools):
        for b in tools[i + 1:]:
            fa, fb = a.get("function", a), b.get("function", b); A, B = toks(fa.get("description", "")), toks(fb.get("description", ""))
            j = len(A & B) / len(A | B) if A | B else 0
            if j >= ov: sims.append({"a": fa.get("name"), "b": fb.get("name"), "jaccard": round(j, 2)}); issues.append({"tool": fa.get("name"), "severity": "alta", "issue": f"Descripcion solapada con '{fb.get('name')}' (Jaccard {j:.2f}): consolidar o diferenciar."})
    sev = {"alta": 0, "media": 0, "baja": 0}
    for i in issues: sev[i["severity"]] += 1
    return {"tools": len(tools), "summary": sev, "overlaps": sims, "issues": issues, "score": max(0, 100 - 15 * sev["alta"] - 6 * sev["media"] - 2 * sev["baja"])}

def describe(s):
    L = [f"## {s['name']}", "", s["purpose"], ""]
    if s.get("use_when"): L += ["**Usar cuando:**"] + [f"- {x}" for x in s["use_when"]] + [""]
    if s.get("avoid_when"): L += ["**No usar cuando:**"] + [f"- {x}" for x in s["avoid_when"]] + [""]
    if s.get("params"): L += ["**Parametros:**"] + [f"- `{k}`: {v}" for k, v in s["params"].items()] + [""]
    if s.get("returns"): L += [f"**Retorna:** {s['returns']}", ""]
    if s.get("errors"): L += ["**Errores y correccion:**"] + [f"- `{k}`: {v}" for k, v in s["errors"].items()]
    return "\n".join(L)

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    l = sub.add_parser("lint"); l.add_argument("file"); l.add_argument("--overlap", type=float, default=0.5)
    d = sub.add_parser("describe"); d.add_argument("file"); a = ap.parse_args(argv); data = json.load(open(a.file))
    print(json.dumps(lint(data, a.overlap), ensure_ascii=False, indent=2) if a.cmd == "lint" else describe(data)); return 0

if __name__ == "__main__": sys.exit(main())
