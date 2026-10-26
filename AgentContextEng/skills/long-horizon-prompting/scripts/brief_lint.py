#!/usr/bin/env python3
"""long-horizon-prompting: lint y plantilla de briefs de tareas pseudo-formales para agentes de larga duracion.

Uso:
  python brief_lint.py lint BRIEF.md
  python brief_lint.py scaffold [--title "..."] > brief.md
Verifica la anatomia: definiciones, predicado de exito exacto, resultados que NO cuentan, reglas de persistencia/parada,
piso de esfuerzo, politica de diversidad/registro de enfoques, auditoria adversarial antes de retornar; y marca lenguaje vago.
"""
import argparse, json, re, sys

SECTIONS = [
    ("definitions", r"(?i)defin|terminolog|glosario|terms", "Define los terminos con precision linguistica."),
    ("success_predicate", r"(?i)success|exito|éxito|predicate|predicado|criterio de (?:exito|éxito)", "Enuncia el predicado de exito exacto."),
    ("non_counting", r"(?i)non-?counting|no cuentan|no cuenta|does not count|outcomes that (?:do not|don't) count|resultados invalidos", "Enumera resultados que NO cuentan como exito."),
    ("persistence", r"(?i)persist|stop|parada|return condition|condici[oó]n de (?:retorno|parada)|no (?:te )?detengas|keep working", "Define cuando continuar, detenerse y retornar."),
    ("effort_floor", r"(?i)effort|esfuerzo|m[ií]nimo de|at least \d+|al menos \d+|minimum", "Fija un piso de esfuerzo antes de rendirse."),
    ("diversity", r"(?i)divers|portfolio|portafolio|registry|registro de enfoques|approach|enfoque|blocked|bloquead", "Politica de diversidad y registro de enfoques."),
    ("audit_gate", r"(?i)audit|adversar|verifier|verificador|red.?team|review gate", "Puerta de auditoria adversarial antes de retornar."),
]
VAGUE = ["try to", "intenta", "best effort", "mejor esfuerzo", "if possible", "si es posible", "probably", "quizas", "quizás", "etc.", "something like", "algo como", "good enough", "suficientemente bueno", "as needed", "segun corresponda", "según corresponda", "reasonable", "razonable"]

def lint(text):
    low = text.lower(); found = []; missing = []
    for k, rx, tip in SECTIONS:
        (found if re.search(rx, text) else missing).append((k, tip))
    vague = [{"term": v, "count": low.count(v)} for v in VAGUE if v in low]
    numbers = len(re.findall(r"\b\d+\b", text)); musts = len(re.findall(r"(?i)\b(must|shall|debes|debe|nunca|never|only if|solo si)\b", text))
    score = round(100 * len(found) / len(SECTIONS) - min(25, 5 * sum(v["count"] for v in vague)))
    advice = [t for _, t in missing] + [f"Reemplazar lenguaje vago: '{v['term']}' ({v['count']}x)." for v in vague]
    if numbers == 0: advice.append("Sin cifras: fija umbrales concretos (iteraciones, tiempo, numero de enfoques).")
    if musts == 0: advice.append("Sin obligaciones explicitas (debe/nunca/solo si): el agente puede interpretar libremente.")
    return {"words": len(text.split()), "score": max(0, score), "present": [k for k, _ in found], "missing": [k for k, _ in missing], "vague_language": vague, "numbers_found": numbers, "advice": advice,
            "verdict": "listo" if score >= 85 and not missing else "mejorar antes de lanzar"}

TEMPLATE = """# Brief de tarea: {title}

## 1. Definiciones
- <termino>: <definicion linguistica precisa; sin ambiguedad>

## 2. Predicado de exito exacto
La tarea tiene exito si y solo si se cumplen TODAS: (a) ... (b) ... (c) ...

## 3. Resultados que NO cuentan como exito
- Un artefacto con apariencia de respuesta pero que ... 
- Una demostracion/solucion que solo cubre casos ...
- Reducciones a un problema equivalente no resuelto.

## 4. Persistencia y condiciones de retorno
- Continua trabajando hasta que se cumpla el predicado o se declare bloqueo con evidencia.
- Solo retorna si: (1) predicado cumplido y auditado, o (2) se agotaron N=<numero> enfoques distintos documentados.
- Nunca declares exito sin pasar la auditoria de la seccion 7.

## 5. Piso de esfuerzo
- Al menos <N> intentos sustantivos y <M> enfoques distintos antes de considerar un bloqueo.

## 6. Politica de diversidad y registro de enfoques
- Mantener un registro: enfoque, estado (activo/bloqueado/agotado), motivo de bloqueo.
- Cada worker paralelo debe usar un enfoque distinto del registro; prohibido repetir rutas bloqueadas.

## 7. Puerta de auditoria adversarial
- Un auditor independiente intenta refutar el resultado contra las secciones 2 y 3 antes del retorno.
- Si el auditor encuentra una falla, volver a la seccion 4.

## 8. Formato de entrega
- <estructura exacta del resultado>
"""

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True); l = sub.add_parser("lint"); l.add_argument("file"); s = sub.add_parser("scaffold"); s.add_argument("--title", default="<titulo>")
    a = ap.parse_args(argv)
    if a.cmd == "lint": print(json.dumps(lint(open(a.file, encoding="utf-8").read()), ensure_ascii=False, indent=2))
    else: print(TEMPLATE.format(title=a.title))
    return 0

if __name__ == "__main__": sys.exit(main())
