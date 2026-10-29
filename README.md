# proyectosML — Metodología y Línea Base Universal para Desarrollo Asistido por IA

[![Licencia: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Metodología: ICM](https://img.shields.io/badge/Methodology-ICM-blue.svg)](https://github.com/RinDig/Interpretable-Context-Methodology)
[![Compatibilidad: Universal AI](https://img.shields.io/badge/AI_Tools-Antigravity_%7C_Claude_Code_%7C_Cursor_%7C_Windsurf_%7C_Copilot-purple.svg)](#-compatibilidad-universal-con-herramientas-de-ia)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

**proyectosML** es un marco de trabajo de código abierto (*open-source framework*) que implementa el patrón **Umbrella** de la metodología **ICM (Interpretable Context Methodology)** para estructurar, estandarizar y gobernar proyectos de **Ciencia de Datos**, **Machine Learning Productivo** y **Desarrollo Agéntico**, haciéndolos **compatibles de forma nativa con cualquier asistente de programación con IA** (*Google Antigravity, Claude Code, Cursor, Windsurf, GitHub Copilot, Aider, etc.*).

---

## 🎯 ¿Por qué nace este proyecto? (El Problema Real)

Desarrollar soluciones de Machine Learning o Ciencia de Datos con asistentes de IA actuales suele toparse con 5 cuellos de botella críticos:

1. **Context Rot (Degradación de Contexto)**: Los proyectos de datos acumulan CSVs pesados, notebooks gigantescos con gráficos en base64 y código desordenado. Cuando el agente lee decenas de miles de tokens, empieza a alucinar y olvidar directrices clave.
2. **Data Leakage (Fuga de Datos)**: Los LLMs frecuentemente ajustan transformaciones sobre el dataset completo o ignoran la temporalidad en series de tiempo al no tener barreras físicas en el sistema de archivos.
3. **Pérdida del Sustento Teórico**: Las decisiones matemáticas, funciones de pérdida y formulaciones se discuten en el chat de la IA y se pierden, dejando el código huérfano de justificación científica.
4. **Fricción Multi-Herramienta**: Cada herramienta de IA exige su propio archivo de configuración (`CLAUDE.md`, `.cursorrules`, `AGENTS.md`, `copilot-instructions.md`), provocando fragmentación y duplicidad.
5. **Notebook Spaghetti**: Flujos exploratorios que dependen del estado en memoria RAM del kernel y resultan imposibles de reproducir semanas después.

---

## 💡 Los 4 Pilares de la Solución

1. **La Estructura de Carpetas como Arquitectura (ICM)**: En lugar de frameworks pesados, el sistema de archivos orquesta al modelo mediante contratos de etapa explícitos (`CONTEXT.md`) y una disciplina estricta de **2.000 a 8.000 tokens por interacción**.
2. **Single Source of Truth + Adaptadores Universales**: Un único archivo de reglas canónicas (`AGENTS.md`) respaldado por adaptadores automáticos para Claude Code, Cursor, Windsurf y Copilot.
3. **Anclaje Teórico (`research/`)**: Una carpeta formal de primer nivel para alojar la formulación matemática en LaTeX, estado del arte, justificación metodológica y bitácora de hipótesis.
4. **Inmutabilidad y Gestión de Datos por Capas**: Datos crudos (`data/raw/`) estrictamente de solo lectura, procesados en capas (`interim/`, `processed/`) y protegidos en Git mediante `.gitignore` calibrado.

---

## 🤖 Compatibilidad Universal con Herramientas de IA

Cualquier proyecto creado dentro de `proyectosML` se adapta automáticamente a tu entorno de trabajo favorito:

| Asistente / Herramienta | Archivo de Configuración | Cómo Opera |
| :--- | :--- | :--- |
| **Google Antigravity** | `AGENTS.md` + `~/.gemini/config/GEMINI.md` | Carga las reglas universales, disciplina de tokens y ejecuta las skills globales. |
| **Claude Code (CLI)** | `CLAUDE.md` + `~/.claude/skills/` | Enrutamiento en raíz y acceso directo a las skills globales (`icm-architect`, `project-scaffold`). |
| **Cursor IDE** | `.cursorrules` (en raíz y en cada proyecto) | Aplica las restricciones de datos inmutables y contratos en cada interacción de chat o *Composer*. |
| **Windsurf / Cascade** | `.windsurfrules` (en raíz y en cada proyecto) | Dirige al motor Cascade a respetar la inmutabilidad y los contratos ICM. |
| **GitHub Copilot** | `.github/copilot-instructions.md` | Instrucciones automáticas para Copilot Chat en VS Code, JetBrains o GitHub.com. |
| **Aider / Codex / Open Source** | `AGENTS.md` + `CONTEXT.md` | Estándar abierto de agentes CLI. |

---

## 🚀 Inicio Rápido (En 60 Segundos)

### 1. Clonar el Repositorio
```bash
git clone https://github.com/f-marchant/proyectosML.git
cd proyectosML
```

### 2. Ejecutar el Instalador Universal (`bootstrap.sh`)
```bash
chmod +x bootstrap.sh
./bootstrap.sh
```
*Este comando vincula automáticamente las reglas y las skills globales tanto a Google Antigravity como a Claude Code.*

### 3. Crear tu Primer Proyecto Estandarizado
```bash
# 🔬 Para Ciencia de Datos (con research/ y capas de datos):
./init-project.sh scoring-crediticio --type ds "Modelo de riesgo con LightGBM"

# ⚙️ Para Machine Learning Productivo (API FastAPI + Docker):
./init-project.sh api-deteccion --type ml "Microservicio de inferencia en tiempo real"

# 🤖 Para Desarrollo Agéntico (Prompts + Tools + Evals):
./init-project.sh analista-autonomo --type agentic "Agente con herramientas de búsqueda y RAG"
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
└── reports/ (summary.md)           └── deployment/
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
@software{marchant2026proyectosml,
  author       = {Marchant, Felipe},
  title        = {proyectosML: A Universal Agentic Baseline & Workspace Architecture for Data Science, Machine Learning, and AI Engineering},
  year         = {2026},
  publisher    = {GitHub},
  journal      = {GitHub repository},
  howpublished = {\url{https://github.com/f-marchant/proyectosML}}
}
```

### Formato APA (7.ª edición):
> Marchant, F. (2026). *proyectosML: A Universal Agentic Baseline & Workspace Architecture for Data Science, Machine Learning, and AI Engineering* [Computer software]. GitHub. https://github.com/f-marchant/proyectosML

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
- **[Agent Skills for Context Engineering](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering)** por Muratcan Koylan (Licencia MIT).
  - *Base del subproyecto `AgentContextEng`*.

---

## ⚖️ Licencia y Contribuciones

Este proyecto se distribuye bajo la **[Licencia MIT](LICENSE)**. Las contribuciones de la comunidad son bienvenidas; por favor revisa la [Guía de Contribución](CONTRIBUTING.md) antes de enviar un Pull Request.
