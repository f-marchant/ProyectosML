# proyectosML — Metodología y Línea Base Universal para Desarrollo Asistido por IA

[![Licencia: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Metodología: ICM](https://img.shields.io/badge/Methodology-ICM-blue.svg)](https://github.com/RinDig/Interpretable-Context-Methodology)
[![Compatibilidad: Universal AI](https://img.shields.io/badge/AI_Tools-Antigravity_%7C_Claude_Code_%7C_Cursor_%7C_Windsurf_%7C_Copilot-purple.svg)](#-compatibilidad-con-herramientas-de-ia)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

**proyectosML** es un marco de trabajo de código abierto (*open-source framework*) que implementa el patrón **Umbrella** de la metodología **ICM (Interpretable Context Methodology)** para estructurar, estandarizar y gobernar proyectos de **Ciencia de Datos**, **Machine Learning Productivo** y **Desarrollo Agéntico**. Está diseñado para operar de forma consistente con los principales asistentes de programación con IA (*Google Antigravity, Claude Code, Cursor, Windsurf, GitHub Copilot, Aider*), mediante adaptadores generados a partir de una única fuente de verdad canónica (`AGENTS.md`).

---

## 🎯 ¿Por qué nace este proyecto? (El Problema Real)

Desarrollar soluciones de Machine Learning o Ciencia de Datos asistidas por agentes LLM enfrenta cinco cuellos de botella críticos:

1. **Context Rot (Degradación de Contexto)**: Los proyectos de datos acumulan CSVs masivos, notebooks con gráficos en base64 y código exploratorio redundante. Cuando el agente ingiere decenas de miles de tokens, incrementa el riesgo de alucinación y dilución de directrices.
2. **Data Leakage (Fuga de Datos)**: Sin barreras explícitas en el sistema de archivos y validaciones automatizadas, los asistentes suelen ajustar transformaciones (`fit`) sobre el dataset completo o ignorar el orden temporal en series de tiempo.
3. **Pérdida del Sustento Teórico**: Las formulaciones matemáticas, funciones de pérdida y justificaciones de arquitectura quedan dispersas en el historial efímero del chat, desvinculadas del código final.
4. **Fricción Multi-Herramienta**: Cada entorno exige formatos propietarios de configuración (`CLAUDE.md`, `.cursorrules`, `.cursor/rules/*.mdc`, `.windsurfrules`, `.github/copilot-instructions.md`), generando duplicidad y reglas desincronizadas.
5. **Notebook Spaghetti y Falta de Reproducibilidad**: Flujos interactivos que dependen del estado en memoria del kernel, difíciles de auditar o trasladar a pipelines de producción.

---

## 💡 Los 4 Pilares de la Solución

1. **La Estructura de Carpetas como Arquitectura (ICM)**: En lugar de orquestadores complejos, el sistema de archivos guía al modelo mediante contratos de etapa explícitos (`CONTEXT.md`) y una disciplina estricta de presupuesto de contexto (**2.000 a 8.000 tokens por interacción**).
2. **Single Source of Truth (`AGENTS.md`) + Adaptadores Sincronizados**: Las reglas maestras residen en un único archivo canónico (`AGENTS.md`). El script `./sync-adapters.sh` propaga automáticamente estas directrices hacia Claude Code, Cursor (soporte moderno `.mdc` y clásico `.cursorrules`), Windsurf y Copilot.
3. **Anclaje Teórico (`research/`)**: Un módulo formal de primer nivel para alojar formulaciones matemáticas en KaTeX ($\mathcal{X} \to \mathcal{Y}$), comparativas del estado del arte, justificación metodológica y bitácora de hipótesis (`hypothesis_log.md`).
4. **Convención de Inmutabilidad y Datos por Capas**: Establece `data/raw/` como capa de solo lectura por convención metodológica, promoviendo el flujo unidireccional hacia `interim/` y `processed/`, complementado con tests unitarios automatizados y protección de artefactos pesados en `.gitignore`.

---

## 🤖 Compatibilidad con Herramientas de IA

Los proyectos creados bajo `proyectosML` se integran con diversos entornos mediante adaptadores sincronizados:

| Asistente / Herramienta | Archivo(s) de Configuración | Nivel de Soporte | Cómo Opera |
| :--- | :--- | :---: | :--- |
| **Google Antigravity** | `AGENTS.md` + `~/.gemini/config/GEMINI.md` | **Nativo / Global** | Carga reglas globales, disciplina de tokens y ejecuta catálogo de skills (`_baseline/skills/`). |
| **Claude Code (CLI)** | `CLAUDE.md` + `~/.claude/skills/` | **Adaptador Sincronizado** | Enrutamiento optimizado para CLI y acceso a skills globales del usuario. |
| **Cursor IDE** | `.cursor/rules/main.mdc` y `.cursorrules` | **Adaptador Sincronizado** | Compatible con el formato moderno de reglas `.mdc` y retrocompatible con `.cursorrules`. |
| **Windsurf / Cascade** | `.windsurfrules` | **Adaptador Sincronizado** | Instruye al motor Cascade para respetar contratos ICM e inmutabilidad de datos. |
| **GitHub Copilot** | `.github/copilot-instructions.md` | **Adaptador Sincronizado** | Provee contexto a Copilot Chat en VS Code, JetBrains y GitHub.com. |
| **Aider / Agentes CLI** | `AGENTS.md` + `CONTEXT.md` | **Estándar Abierto** | Lee especificaciones markdown estándar directamente desde el workspace. |

### 🛠️ Skills Integradas en la Línea Base (`_baseline/skills/`)

El framework incluye un conjunto curado de skills nativas (estándar abierto `SKILL.md`) diseñadas para eliminar el "vibe coding" y forzar rigor de ingeniería:

| Skill | Ámbito | Descripción |
| :--- | :--- | :--- |
| **`grill-me`** | Transversal | Entrevista exhaustiva por rondas para desafiar supuestos, clarificar trade-offs y pulir decisiones de diseño antes de escribir código. |
| **`diagnose`** | Transversal | Disciplina metódica de 6 fases para aislar y resolver bugs difíciles o regresiones de rendimiento (incluye script HITL). |
| **`handoff`** | Transversal | Compacta la sesión en un artefacto estructurado para reanudar el trabajo en una nueva sesión dentro del presupuesto de tokens (2k–8k). |
| **`retro`** | Transversal | Retrospectiva post-sesión para identificar fricciones, optimizar el uso de herramientas y alimentar las reglas en `AGENTS.md`. |
| **`icm-architect`**| Transversal | Diseña y audita espacios de trabajo bajo los 6 arquetipos formales de la metodología ICM. |
| **`project-scaffold`** | Transversal | Inicializa y estandariza nuevos proyectos (`ds`, `ml`, `agentic`) con sus contratos de contexto y tests. |
| **`to-spec`** | Agéntico | Sintetiza el diseño acordado en una especificación técnica formal y estructurada (historias, interfaces y evals). |
| **`to-tickets`** | Agéntico | Descompone una especificación en un grafo de tickets ejecutables (rebanadas verticales *tracer bullets* con dependencias). |
| **`implement-spec`**| Agéntico | Orquesta la construcción de la frontera de tickets con subagentes independientes y ventanas de contexto limpias. |


---

## 🚀 Inicio Rápido (En 60 Segundos)

### 1. Clonar el Repositorio
```bash
git clone https://github.com/f-marchant/ProyectosML.git
cd ProyectosML
```

### 2. Configurar el Entorno Global y Permisos (`bootstrap.sh`)
```bash
chmod +x bootstrap.sh init-project.sh sync-adapters.sh
./bootstrap.sh
```
> [!NOTE]
> **Alcance de `bootstrap.sh`**: Configura a nivel de sistema los enlaces simbólicos de reglas y skills para **Google Antigravity** (`~/.gemini/`) y **Claude Code CLI** (`~/.claude/`). Adicionalmente, ejecuta `sync-adapters.sh` para asegurar que los adaptadores de Cursor, Windsurf y Copilot estén sincronizados en la raíz del repositorio.

### 3. Crear tu Primer Proyecto Estandarizado (`init-project.sh`)
```bash
# Para Ciencia de Datos (con research/, capas de datos y validadores):
./init-project.sh scoring-crediticio --type ds "Modelo de riesgo con LightGBM"

# Para Machine Learning Productivo (API FastAPI + Docker + Pipeline):
./init-project.sh api-deteccion --type ml "Microservicio de inferencia en tiempo real"

# Para Desarrollo Agéntico (Prompts + Tools + Evals + Grafos):
./init-project.sh analista-autonomo --type agentic "Agente con herramientas de búsqueda y RAG"
```

### 4. Sincronizar Reglas entre Asistentes (`sync-adapters.sh`)
Si realizas ajustes en las directrices de `AGENTS.md`, propágalos a todos los adaptadores ejecutando:
```bash
# Sincronizar la raíz del workspace:
./sync-adapters.sh

# O sincronizar un proyecto específico:
./sync-adapters.sh projects/scoring-crediticio
```

---

## 🧪 Suite de Validación y Pruebas Unitarias

Cada proyecto incluye herramientas de verificación técnica para asegurar buenas prácticas de ingeniería:

1. **`tests/test_data_leakage.py`**:
   Verifica que los pipelines de preprocesamiento ajusten sus transformaciones (`fit`) exclusivamente sobre los datos de entrenamiento y no filtren estadísticas del conjunto de validación o test.
2. **`tests/test_git_hygiene.py`**:
   Inspecciona el árbol git local y previene que se comiteen archivos binarios pesados (`.pkl`, `.joblib`, `.pt`), datasets masivos o artefactos que degraden el repositorio.
3. **`scripts/check_context_budget.py`**:
   Script CLI que calcula el consumo estimado de tokens en los archivos de directrices y contratos (`AGENTS.md`, `CLAUDE.md`, `CONTEXT.md`), alertando si se excede el presupuesto objetivo de 2.000 a 8.000 tokens de la metodología ICM.

Para ejecutar los tests de un proyecto:
```bash
# Ejecutar suite de pruebas unitarias:
pytest projects/scoring-crediticio/tests/

# Auditar presupuesto de tokens de contexto:
python3 projects/scoring-crediticio/scripts/check_context_budget.py
```

---

## 📊 Comparativa de los 3 Arquetipos de Proyectos

```text
🔬 CIENCIA DE DATOS (ds)            ⚙️ ML PRODUCTIVO (ml)              🤖 AGÉNTICO (agentic)
─────────────────────────────────   ────────────────────────────────   ──────────────────────────────────
projects/mi-analisis/               projects/mi-servicio-ml/           projects/mi-agente/
├── AGENTS.md / CLAUDE.md           ├── AGENTS.md / CLAUDE.md          ├── AGENTS.md / CLAUDE.md
├── .cursorrules / .windsurfrules   ├── .cursorrules / .windsurfrules  ├── .cursorrules / .windsurfrules
├── CONTEXT.md                      ├── CONTEXT.md                     ├── CONTEXT.md
│                                   │                                  │
├── _context/                       ├── _context/                      ├── _context/
│   ├── domain.md (variables)       │   ├── api_specs.md (endpoints)   │   ├── persona.md (rol del agente)
│   ├── architecture.md             │   ├── architecture.md (pipeline) │   ├── architecture.md (grafo)
│   └── conventions.md (estadística)│   └── conventions.md (estilo)    │   └── safety_guardrails.md
│                                   │                                  │
├── research/ (🧠 Sustento Teórico) ├── data/ (sample y schemas)       ├── prompts/ (system y templates)
│   ├── 01_problem_formulation.md   │                                  ├── tools/ (schemas + código)
│   ├── 02_literature_review.md     ├── src/                           ├── memory/ (sesiones + RAG)
│   ├── 03_methodological_rationale │   ├── api/ (FastAPI)             ├── evals/ (golden benchmarks)
│   └── notes/hypothesis_log.md     │   ├── pipeline/ (entrenamiento)  └── logs/traces/ (observabilidad)
│                                   │   └── inference/ (predicción)
├── data/ (raw, interim, processed) │
├── notebooks/ (01_eda a 04_eval)   ├── tests/ (unit e integration)
├── src/ (data, features, models)   ├── Dockerfile
├── tests/ (data leakage e higiene) └── deployment/
├── scripts/ (check context budget)
└── reports/ (summary.md)
```

---

## 🧠 El Sustento Teórico en Ciencia de Datos (`research/`)

Cada proyecto de Ciencia de Datos incluye una estructura formal para anclar el código a la teoría:
- **`01_problem_formulation.md`**: Definición matemática formal en KaTeX ($\mathcal{X} \to \mathcal{Y}$), espacios de hipótesis y funciones de pérdida.
- **`02_literature_review.md`**: Tabla comparativa del estado del arte y papers analizados.
- **`03_methodological_rationale.md`**: Registro estructurado de por qué se eligió un algoritmo, métrica o split específico.
- **`notes/hypothesis_log.md`**: Bitácora de pensamiento e hipótesis planteadas (manuales o asistidas por IA) y su validación empírica.
- **`references/sources.bib`**: Archivo BibTeX consolidado con citas formales.

---

## 📖 Cómo Citar este Trabajo

Si utilizas este espacio de trabajo, sus plantillas o su metodología en tu investigación, tesis o proyecto, por favor cítalo de la siguiente forma:

### Formato BibTeX:
```bibtex
@misc{marchant2026proyectosml,
  author       = {Marchant, Felipe},
  title        = {proyectosML: A Universal Agentic Baseline \& Workspace Architecture for Data Science, Machine Learning, and AI Engineering},
  year         = {2026},
  publisher    = {GitHub},
  howpublished = {\url{https://github.com/f-marchant/ProyectosML}},
  note         = {GitHub repository}
}
```

### Formato APA (7.ª edición):
> Marchant, F. (2026). *proyectosML: A Universal Agentic Baseline & Workspace Architecture for Data Science, Machine Learning, and AI Engineering* [Computer software]. GitHub. https://github.com/f-marchant/ProyectosML

---

## 🤝 Autor y Reconocimientos

- **Autor**: [Felipe Marchant](https://github.com/f-marchant)
- **LinkedIn**: [felipemarchant](https://linkedin.com/in/felipemarchant)

### Fuentes Canónicas y Metodologías Base:
Este repositorio implementa y extiende conceptos fundamentales de la literatura de software e IA:
- **[Interpretable Context Methodology (ICM)](https://github.com/RinDig/Interpretable-Context-Methodology)** por RinDig (arXiv:2603.16021, Licencia MIT).
  - *Base conceptual*: Sustitución de orquestadores complejos por estructura de sistema de archivos, contratos de etapa y disciplina de tokens.
- **[icm-architect](https://github.com/RinDig/icm-architect)** por RinDig (Licencia MIT).
  - *Skill integrada*: Diseñador y auditor de workspaces en los 6 arquetipos formales.
- **[Cookiecutter Data Science](https://github.com/drivendata/cookiecutter-data-science)** por DrivenData (Licencia BSD-3-Clause).
  - *Estructura modular de datos por capas (`data/raw`, `data/interim`, `data/processed`)*.
- **[skills](https://github.com/mattpocock/skills)** por Matt Pocock (Licencia MIT).
  - *Inspiración metodológica*: Patrones de SDLC riguroso para agentes, entrevistas anti-supuestos (`grill-me`), depuración sistemática (`diagnose`), traspasos limpios (`handoff`), retrospectivas (`retro`) y ciclo agéntico spec-tickets-implementación.

---

## ⚖️ Licencia y Contribuciones

Este proyecto se distribuye bajo la **[Licencia MIT](LICENSE)**. Las contribuciones de la comunidad son bienvenidas; por favor revisa la [Guía de Contribución](CONTRIBUTING.md) antes de enviar un Pull Request.
