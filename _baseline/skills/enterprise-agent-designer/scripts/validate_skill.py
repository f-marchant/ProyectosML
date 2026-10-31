#!/usr/bin/env python3
"""Validación estática exhaustiva del paquete de la skill (v7.3.0).

Uso:  python3 -I scripts/validate_skill.py [ruta_raiz_de_la_skill]
"""
import os
import re
import sys

root = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.abspath(
    os.path.join(os.path.dirname(__file__), ".."))
errors, warnings = [], []


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


skill_path = os.path.join(root, "SKILL.md")
if not os.path.exists(skill_path):
    print(f"ERROR: no existe {skill_path}")
    sys.exit(1)
s = read(skill_path)

# 1. Frontmatter
fm = re.match(r"^---\n(.*?)\n---\n", s, re.S)
if not fm:
    errors.append("SKILL.md sin frontmatter")
else:
    for key in ("name", "description", "version", "language"):
        m = re.search(rf"^{key}:\s*(.+)$", fm.group(1), re.M)
        if not m:
            errors.append(f"Frontmatter sin campo '{key}'")
        elif key == "version" and m.group(1).strip() != "7.3.0":
            errors.append(f"Frontmatter con version '{m.group(1).strip()}', se esperaba '7.3.0'")

# 2. Bloques balanceados
named = ["WORKER", "ENUM", "PRINCIPLES", "VARIABLES", "CONSTRAINTS",
         "SKILL_WORKFLOW", "FORMAT", "SKILL_RESULT"]
for k in named:
    a = len(re.findall(rf"\[DEFINE_{k}[:\]\s]", s))
    b = len(re.findall(rf"\[END_{k}\]", s))
    if a != b:
        errors.append(f"Bloque {k} desbalanceado en SKILL.md: {a} aperturas, {b} cierres")
for k in ("INPUTS", "OUTPUTS", "SEQUENTIAL_BLOCK"):
    a = len(re.findall(rf"^\[{k}\]", s, re.M))
    b = len(re.findall(rf"^\[END_{k}\]", s, re.M))
    if a != b:
        errors.append(f"Bloque {k} desbalanceado en SKILL.md: {a} aperturas, {b} cierres")

# 3. Referencias citadas
refs = set(re.findall(r"references/[\w/]+\.md", s))
for r in sorted(refs):
    if not os.path.exists(os.path.join(root, r)):
        errors.append(f"Referencia inexistente: {r}")

# 4. Variables declaradas en Sección 8
vm = re.search(r"\[DEFINE_VARIABLES:\](.*?)\[END_VARIABLES\]", s, re.S)
declared_vars = set()
if vm:
    declared_vars = set(re.findall(r"^- ([a-z][a-z0-9_]*):", vm.group(1), re.M))
else:
    errors.append("Sin bloque DEFINE_VARIABLES")

# 5. WORKERS y flujo
workflow = re.search(r"\[DEFINE_SKILL_WORKFLOW:.*?\](.*?)\[END_SKILL_WORKFLOW\]", s, re.S)
called = re.findall(r"CALL WORKER:\s*(\w+)", workflow.group(1)) if workflow else []
sec = s.split("## 10. WORKERS", 1)[-1].split("## 11. ", 1)[0]
blocks = re.split(r"(?=### WORKER \d+: )", sec)[1:]
defined = []
worker_inputs = {}
worker_outputs = {}

for b in blocks:
    m = re.match(r"### WORKER (\d+): (\w+)", b)
    num, name = m.group(1), m.group(2)
    defined.append(name)
    if f"[DEFINE_WORKER: {name}]" not in b:
        errors.append(f"WORKER {num} {name}: falta DEFINE_WORKER con el mismo nombre")
    if not re.search(r"\*\*Objetivo\*\*:", b):
        errors.append(f"WORKER {num} {name}: sin Objetivo")
    
    i = re.search(r"\[INPUTS\](.*?)\[END_INPUTS\]", b, re.S)
    o = re.search(r"\[OUTPUTS\](.*?)\[END_OUTPUTS\]", b, re.S)
    if not i or not o:
        errors.append(f"WORKER {num} {name}: falta INPUTS u OUTPUTS")
        continue

    # Validar formato de INPUTS
    ins = []
    for line in i.group(1).strip().splitlines():
        if line.strip().startswith("-"):
            var_name = line.strip().lstrip("- ").strip()
            if not re.match(r"^[a-z][a-z0-9_]*$", var_name):
                errors.append(f"WORKER {num} {name}: INPUT no cumple snake_case estricto: '{var_name}'")
            ins.append(var_name)
    worker_inputs[name] = ins

    # Validar formato de OUTPUTS
    outs = []
    for line in o.group(1).strip().splitlines():
        if line.strip().startswith("-"):
            var_name = line.strip().lstrip("- ").strip()
            if not re.match(r"^[a-z][a-z0-9_]*$", var_name):
                errors.append(f"WORKER {num} {name}: OUTPUT no cumple snake_case estricto: '{var_name}'")
            if var_name not in declared_vars:
                errors.append(f"WORKER {num} {name}: OUTPUT '{var_name}' no declarado en [DEFINE_VARIABLES]")
            outs.append(var_name)
    worker_outputs[name] = outs

    # Archivo de detalle del WORKER
    fn = f"references/workers/Worker_{num}_{name}.md"
    fp = os.path.join(root, fn)
    if fn not in s:
        errors.append(f"WORKER {num} {name}: SKILL.md no apunta a {fn}")
    if not os.path.exists(fp):
        errors.append(f"WORKER {num} {name}: falta {fn}")
    else:
        w = read(fp)
        if not (w.count("[SEQUENTIAL_BLOCK]") == w.count("[END_SEQUENTIAL_BLOCK]") == 1):
            errors.append(f"{fn}: SEQUENTIAL_BLOCK ausente o duplicado")
        steps = re.findall(r"^\d+\. ", w, re.M)
        if len(steps) < 3:
            errors.append(f"{fn}: menos de 3 pasos numerados")
        if "**Versión**: 7.3.0" not in w:
            errors.append(f"{fn}: version no sincronizada a 7.3.0")

if len(defined) != 23:
    errors.append(f"Se esperaban 23 WORKERS y hay {len(defined)}")
if len(set(defined)) != len(defined):
    errors.append("Nombres de WORKER duplicados")
for n in called:
    if n not in defined:
        errors.append(f"El flujo invoca WORKER no definido: {n}")
for n in defined:
    if n not in called:
        errors.append(f"WORKER definido y no invocado en el flujo: {n}")

# 6. Verificación de resolución de INPUTS en el orden del workflow
available = set(declared_vars)
produced_so_far = set()

if called and called[0] != "Understand_Request":
    errors.append(f"El flujo debe iniciar con Understand_Request (inició con {called[0]})")

for wname in called:
    ins = worker_inputs.get(wname, [])
    for v in ins:
        if v not in available and v not in produced_so_far:
            errors.append(f"WORKER {wname}: INPUT '{v}' no disponible en el ámbito ni producido previamente")
    outs = worker_outputs.get(wname, [])
    produced_so_far |= set(outs)

if "delivery_plan" not in produced_so_far:
    errors.append("Variable 'delivery_plan' nunca producida por ningún WORKER")
if "correction_log" not in produced_so_far:
    errors.append("Variable 'correction_log' nunca producida por ningún WORKER")

# 7. Variables declaradas sin uso
all_used = set()
for ins in worker_inputs.values():
    all_used |= set(ins)
for outs in worker_outputs.values():
    all_used |= set(outs)

unused_vars = declared_vars - all_used
for v in sorted(unused_vars):
    warnings.append(f"Variable declarada en Sección 8 sin uso en inputs/outputs: {v}")

# 8. Comprobar version en Estándar Maestro
master_std_path = os.path.join(root, "references/Estandar_Maestro_Diseno_Agentes.md")
if os.path.exists(master_std_path):
    m_txt = read(master_std_path)
    if "[VERSION: 7.3.0]" not in m_txt:
        errors.append("references/Estandar_Maestro_Diseno_Agentes.md: versión no sincronizada a 7.3.0")

# 9. Bloques DEFINE/END en todos los archivos markdown de references/
refdir = os.path.join(root, "references")
for dp, _, files in os.walk(refdir):
    for f in files:
        if not f.endswith(".md"):
            continue
        t = read(os.path.join(dp, f))
        for k in ("STANDARD", "CONSTRAINTS", "ENUM", "WORKER", "TYPE"):
            a = len(re.findall(rf"\[DEFINE_{k}[:\]\s]", t))
            b = len(re.findall(rf"\[END_{k}\]", t))
            if a != b and f != "Ejemplo_Agente_Sintetico.md":
                errors.append(f"{os.path.relpath(os.path.join(dp, f), root)}: bloque {k} {a}/{b}")

print(f"WORKERS: {len(defined)} | Variables declaradas: {len(declared_vars)} | Referencias citadas: {len(refs)}")
for w in warnings:
    print("AVISO:", w)
for e in errors:
    print("ERROR:", e)
print("RESULTADO:", "FALLA" if errors else "OK (v7.3.0 Verificada)")
sys.exit(1 if errors else 0)
