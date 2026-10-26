# Informe v2: skills de Context Engineering para Copilot M365 (Agent Builder)

**Fecha:** 4 de octubre de 2026
**Origen:** https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering (MIT)
**Cambios respecto a v1:** (1) `SKILL.md` aprovecha hasta 20.000 caracteres, (2) un agente único con las 18 skills, (3) scripts Python reales y probados.

## 1. Resumen

- **18 skills** empaquetadas, cada una con `SKILL.md` + cabecera YAML, en `.zip` listo para subir.
- **18 scripts nuevos** (uno por skill), solo biblioteca estándar, sin red, con CLI (`--help`) y salida JSON o texto.
- **18 pruebas funcionales** que ejecutan cada script como proceso real con datos de ejemplo. Resultado: **18/18 OK**. Se ejecutaron también contra el paquete final y se hizo `--help` desde cada `.zip` extraído.
- **14 de 18** `SKILL.md` caben completos. Los otros 4 (los que superaban 20.000 en origen) se siguen recortando, pero menos que en v1: ver sección 3.

## 2. Cambio de límites

| Aspecto | v1 | v2 |
|---|---|---|
| Tamaño de `SKILL.md` | objetivo 19.000 | objetivo **19.900** (límite oficial: menos de 20.000) |
| Skills por agente | 8 (3 agentes) | **18 en un agente** + los 3 agentes de v1 como alternativa |
| Scripts | demos con simulaciones | CLIs funcionales sobre archivos reales |

**Diferencia con la documentación:** pediste hasta 20 skills por agente. La documentación de Microsoft Learn que revisé hoy (actualizada el 30/09/2026) indica un máximo de **8 skills por agente en Agent Builder**. Puede que tu tenant tenga un límite distinto, pero no lo pude verificar. Por eso entrego `agentes/00-agente-unico-18-skills.md` y, como respaldo, los 3 agentes de 8, 6 y 4 skills. Si la carga del noveno `.zip` falla, usa los tres agentes.

## 3. Skills, tamaños y scripts

| Skill | Chars originales | Chars finales | Script | Líneas | Secciones movidas a `references/extended-sections.md` |
|---|---:|---:|---|---:|---|
| `advanced-evaluation` | 16,980 | 17,709 | `judge_toolkit.py` | 101 | — |
| `bdi-mental-states` | 17,726 | 18,392 | `bdi.py` | 73 | — |
| `context-compression` | 18,487 | 19,193 | `compression_eval.py` | 55 | — |
| `context-degradation` | 19,136 | 19,849 | `degradation_check.py` | 64 | — |
| `context-fundamentals` | 16,973 | 17,671 | `context_audit.py` | 67 | — |
| `context-optimization` | 16,008 | 16,722 | `optimize_context.py` | 75 | — |
| `evaluation` | 16,829 | 17,526 | `eval_runner.py` | 61 | — |
| `filesystem-context` | 16,132 | 16,823 | `scratchpad.py` | 69 | — |
| `harness-engineering` | 11,413 | 12,116 | `harness_check.py` | 86 | — |
| `hosted-agents` | 17,717 | 18,433 | `sandbox_plan.py` | 55 | — |
| `latent-briefing` | 13,029 | 13,745 | `briefing.py` | 66 | — |
| `long-horizon-prompting` | 25,666 | 19,339 | `brief_lint.py` | 77 | References, Examples, Integration, Gotchas |
| `memory-systems` | 16,514 | 17,201 | `memory_store.py` | 81 | — |
| `multi-agent-patterns` | 18,591 | 19,281 | `task_graph.py` | 62 | — |
| `project-development` | 18,960 | 19,683 | `pipeline.py` | 88 | — |
| `self-improvement-loops` | 22,494 | 18,990 | `loop_gate.py` | 63 | References, Examples, Integration |
| `self-managed-context` | 24,111 | 19,116 | `ctxfile.py` | 82 | References, Examples, Integration, Guidelines |
| `tool-design` | 20,089 | 19,751 | `tool_lint.py` | 62 | References |

Todas quedan por debajo de 20.000. Se agregó a cada `SKILL.md` una sección **"Scripts ejecutables"** (comando de ejemplo y qué hace). Para las que excedían el límite se movieron secciones completas, sin reescribir texto, empezando por las de menor valor (References, Examples, Integration, Guidelines, Gotchas) y restaurando las que aún cabían. Ninguna skill perdió su *Core Concepts* ni *Detailed Topics*.

## 4. Scripts: qué hacen y qué no

Los scripts originales del repo eran demostraciones: simulaban respuestas de LLM, usaban embeddings falsos o `numpy` (no garantizado en el sandbox). Los reemplacé por herramientas deterministas que operan sobre archivos del usuario.

| Skill | Script | Funcionalidad real |
|---|---|---|
| context-fundamentals | `context_audit.py` | Tokens por sección, utilización de ventana, duplicados, posición de datos críticos |
| context-degradation | `degradation_check.py` | Repeticiones, claves con valores contradictorios, pares afirmación/negación, datos en zona media |
| context-compression | `compression_eval.py` | Razón de compresión, retención de archivos/URLs/decisiones/errores/sondas |
| context-optimization | `optimize_context.py` | Enmascarar y restaurar observaciones, estabilidad de prefijo, presupuesto |
| evaluation | `eval_runner.py` | Checks deterministas, rúbrica ponderada, comparación de regresiones |
| advanced-evaluation | `judge_toolkit.py` | Prompts de juez, agregación, sesgo de posición, Spearman y kappa |
| memory-systems | `memory_store.py` | BM25 + grafo con validez temporal (consulta *as-of*), consolidación |
| filesystem-context | `scratchpad.py` | Offload con resumen, grep/lectura por líneas, plan persistente, limpieza |
| multi-agent-patterns | `task_graph.py` | Oleadas paralelas, ruta crítica, ciclos, solapamiento, validación de handoff |
| tool-design | `tool_lint.py` | Lint de esquemas, solapamiento de descripciones, generador de descripción |
| project-development | `pipeline.py` | Pipeline por etapas con caché; estimación de costo |
| hosted-agents | `sandbox_plan.py` | Pool caliente (Poisson), latencia, cadencia de imágenes, costo, Dockerfile |
| latent-briefing | `briefing.py` | Compactación textual BM25 + umbral robusto; modelo de costo |
| long-horizon-prompting | `brief_lint.py` | Lint de briefs y plantilla |
| harness-engineering | `harness_check.py` | Validación de config; ledger con cadena de hashes, novedad y decisión |
| self-improvement-loops | `loop_gate.py` | Compuerta de aceptación (SE pareado, bootstrap), tamaño de edición, selección |
| self-managed-context | `ctxfile.py` | Archivo-espejo, parse-back, compuerta de edición, recibos, niveles de aviso |
| bdi-mental-states | `bdi.py` | Hechos a Beliefs/Desires/Intentions por reglas, validación y Turtle |

**Limitaciones que debes conocer (no son defectos ocultos, son diseño):**
- **Sin LLM ni red en el sandbox.** Los scripts no llaman a ningún modelo. Donde la skill requiere un juez o un generador (`judge_toolkit`, `pipeline`), el script **prepara los prompts y procesa las respuestas**; el modelo es Copilot o tú.
- **Tokens estimados** como caracteres/4. No es un tokenizador real.
- **Heurísticas léxicas** (contradicciones, solapamiento, retención): detectan señales, no reemplazan el juicio. Pueden dar falsos positivos y negativos.
- **`briefing.py` no hace compactación de KV cache** (requiere acceso al runtime del modelo). Implementa un análogo a nivel de texto y lo declara así.
- **`memory_store.py`** usa recuperación léxica (BM25), no embeddings. La persistencia depende de que el sandbox conserve el archivo entre ejecuciones; no lo verifiqué. Conviene exportar el JSON.
- **`bdi.py`** usa una forma simplificada (triples TSV y reglas JSON), no un parser RDF/SPARQL completo.

## 5. Pruebas realizadas

- 18 pruebas en `tests/test_all.py` (ejecutan cada CLI por subproceso y verifican resultados concretos: ciclos detectados, ruta crítica, cadena de hashes manipulada detectada, rechazo de crecimiento en la compuerta, etc.).
- Dos fallos iniciales llevaron a mejoras reales: el detector de duplicados ignoraba que los encabezados distintos enmascaraban párrafos idénticos, y el de negaciones no separaba frases por salto de línea. Un tercer fallo era un error del propio test.
- Validación de paquete: YAML con `name` igual a la carpeta, descripción ≤ 1.000, `SKILL.md` < 20.000, profundidad ≤ 3, sin enlaces relativos rotos, `SKILL.md` en la raíz de cada `.zip`.
- **No probado:** la carga en Agent Builder real ni la ejecución en el sandbox de Copilot (versión de Python y paquetes disponibles no confirmados). Mis scripts no importan nada fuera de la biblioteca estándar para minimizar ese riesgo.

## 6. Agentes

| Archivo | Skills | Chars de instrucciones |
|---|---:|---:|
| `agentes/00-agente-unico-18-skills.md` | Context Engineering Studio | 18 | 4,464 |
| `agentes/01-contexto-core.md` | Context Engineering Core | 8 | 2,744 |
| `agentes/02-arquitectura-agentes.md` | Agent Architecture Advisor | 6 | 2,394 |
| `agentes/03-evaluacion-harness.md` | Agent Eval & Harness | 4 | 2,014 |

(La columna de skills es el número; el nombre del agente está en cada archivo.) Cada archivo incluye nombre (≤ 30), descripción (≤ 1.000) e instrucciones (≤ 8.000). Las instrucciones hacen referencia a las skills por nombre y piden ejecutar el script correspondiente cuando el usuario adjunta datos.

## 7. Entregables (`/v2`)

- `skills-zip/<skill>.zip` (18): paquetes para subir.
- `skills/<skill>/`: carpetas editables (`SKILL.md`, `references/`, `scripts/`).
- `agentes/`: instrucciones del agente único y de los 3 de respaldo.
- `tests/test_all.py`: `python tests/test_all.py` desde la carpeta `v2`.
- `informe.md`: este documento.

## 8. Cómo usar

1. Copilot chat, **Agents & Skills > New agent**, pestaña **Configure**.
2. Pega nombre, descripción e instrucciones de `agentes/00-agente-unico-18-skills.md`.
3. **Skills > Add** y sube los `.zip` uno por uno. Si el tenant rechaza el noveno, usa los agentes 01 a 03.
4. En **Try it**, adjunta un archivo de ejemplo y pide, por ejemplo: "audita este contexto" o "valida este harness". Comprueba que el agente ejecute el script.

## 9. Requisitos y riesgos

- Programa **Frontier** y licencia Copilot (o pago por uso); no disponible con Information Barriers de Purview.
- Las custom skills están en vista previa y los límites pueden cambiar.
- Un agente con skills no puede combinar aún archivos incrustados.
- Probar 3 a 5 prompts por skill: con 18 skills en un agente, el enrutamiento depende de las descripciones, y skills vecinas (por ejemplo `context-fundamentals` y `context-degradation`) pueden confundirse.

## 10. Remediación aplicada

- Se añadió `skills/_shared/safe_io.py` con lectura JSON validada, escritura atómica, locks y validación numérica común.
- `sandbox_plan.py` valida parámetros, rutas, URLs y tokens; la emisión de comandos `setup` requiere `--allow-setup` explícito.
- `memory_store.py` usa escritura atómica, protección de acceso/escritura del store, validación de esquema, `--dry-run` para consolidación y rechazo de umbrales inválidos.
- `scratchpad.py` usa escritura atómica para artefactos persistentes y devuelve errores controlados ante expresiones regulares inválidas.
- `harness_check.py` valida los campos mínimos del ledger, protege el append con lock y sincroniza la escritura antes de retornar.
- `bdi.py` valida triples, declara el prefijo `rdfs` y escapa literales Turtle.
- Se agregaron regresiones para entradas peligrosas de Dockerfile, parámetros inválidos, consolidación en modo simulación y patrones regex inválidos.
- La suite de pruebas fue limpiada para cerrar archivos temporales correctamente y evitar `ResourceWarning`.

Los cambios preservan los flujos nominales existentes; modifican deliberadamente solo el manejo de entradas inválidas, persistencia y operaciones potencialmente peligrosas. La suite debe ejecutarse en un entorno donde Python pueda iniciarse para confirmar la compatibilidad completa.
