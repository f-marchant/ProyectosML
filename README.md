# ProyectosML — Línea Base Universal y Espacio Umbrella con ICM

[![Metodología: ICM](https://img.shields.io/badge/Methodology-ICM-blue.svg)](https://github.com/RinDig/Interpretable-Context-Methodology)
[![Compatibilidad: Universal AI](https://img.shields.io/badge/AI_Tools-Antigravity_%7C_Claude_Code_%7C_Cursor_%7C_Windsurf_%7C_Copilot-purple.svg)](#-compatibilidad-universal-con-herramientas-de-ia)
[![Licencia: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Espacio de trabajo unificado basado en el patrón **Umbrella** de **Interpretable Context Methodology (ICM)** para gestionar proyectos de **Ciencia de Datos**, **Machine Learning Productivo** y **Desarrollo Agéntico** con la misma línea base de ingeniería, reproducibilidad y disciplina de contexto, **compatible de forma nativa con cualquier asistente o herramienta de IA para programación**.

---

## 🤖 Compatibilidad Universal con Herramientas de IA

Cada proyecto e interactuador en `proyectosML` implementa la arquitectura **Single Source of Truth** con adaptadores específicos para cada herramienta del mercado:

| Asistente / Herramienta | Archivo de Configuración | Cómo Opera |
| :--- | :--- | :--- |
| **Google Antigravity** | `AGENTS.md` + `~/.gemini/config/GEMINI.md` | Lee reglas jerárquicas y ejecuta skills de `_baseline/skills/`. |
| **Claude Code (CLI)** | `CLAUDE.md` + `~/.claude/skills/` | Enrutamiento en raíz y acceso directo a las skills globales. |
| **Cursor IDE** | `.cursorrules` (en raíz y en cada proyecto) | Aplica los contratos de etapa y restricciones de datos en cada chat o *Composer*. |
| **Windsurf / Cascade** | `.windsurfrules` (en raíz y en cada proyecto) | Dirige al motor Cascade a respetar la inmutabilidad y los contratos ICM. |
| **GitHub Copilot** | `.github/copilot-instructions.md` | Instrucciones de contexto automáticas para Copilot Chat en VS Code/JetBrains. |
| **Aider / Codex / Open Source** | `AGENTS.md` + `CONTEXT.md` | Convención abierta de agentes para CLI. |

---

## 🌟 Características Principales

1. **Línea Base Unificada (Patrón Umbrella)**:
   - Configuración global para Antigravity (`~/.gemini/config/GEMINI.md`) y Claude Code (`~/.claude/skills/`).
   - Incorporación nativa de la skill [`icm-architect`](https://github.com/RinDig/icm-architect) para diseñar y auditar workspaces.
   - Aislamiento total entre proyectos: cero contaminación cruzada de dependencias o contexto.
2. **Tres Arquetipos de Proyectos Especializados**:
   - 🔬 **Ciencia de Datos (`ds`)**: Capas de datos (`raw/`, `interim/`, `processed/`), notebooks cronológicos, código modular y carpeta dedicada **`research/`** para formulación matemática y estado del arte.
   - ⚙️ **Machine Learning Productivo (`ml`)**: Pipelines de reentrenamiento, servicio web con FastAPI, validación con Pydantic, tests unitarios/integración y `Dockerfile`.
   - 🤖 **Desarrollo Agéntico (`agentic`)**: Gestión de `prompts/`, catálogo de `tools/` (JSON schemas + implementación), banco de `evals/`, memoria y trazas de observabilidad.
3. **Automatización en 1 Comando**:
   - `init-project.sh`: Script CLI para instanciar cualquier proyecto con su contrato de contexto completo y adaptadores para todas las IAs en 2 segundos.
4. **Portabilidad y Respaldo Total**:
   - `bootstrap.sh`: Configura Antigravity y Claude Code en cualquier máquina personal nueva en menos de 1 minuto.

---

## 🚀 Inicio Rápido

### 1. Inicializar la Línea Base en tu Máquina
Si acabas de clonar este repositorio en una máquina nueva:
```bash
cd ~/proyectosML
./bootstrap.sh
```
El script vinculará automáticamente las reglas y skills a tu configuración global de Antigravity (`~/.gemini/config/`) y Claude Code (`~/.claude/skills/`).

---

### 2. Crear un Nuevo Proyecto

Para crear un nuevo proyecto, ejecuta `init-project.sh` especificando el nombre y el tipo:

```bash
# 🔬 Para un proyecto de Ciencia de Datos (con research/ y capas de datos):
./init-project.sh riesgo-credito --type ds "Modelo predictivo de riesgo crediticio con LightGBM"

# ⚙️ Para un proyecto de Machine Learning con API productiva:
./init-project.sh api-recomendacion --type ml "Microservicio de recomendaciones FastAPI"

# 🤖 Para un proyecto de Agentes Autónomos con tools y evals:
./init-project.sh agente-investigador --type agentic "Agente autónomo con herramientas de búsqueda"
```

El script se encargará de:
1. Copiar la plantilla correspondiente dentro de `projects/<nombre-proyecto>/`.
2. Generar todos los adaptadores de IA (`AGENTS.md`, `CLAUDE.md`, `.cursorrules`, `.windsurfrules`, `.github/copilot-instructions.md`).
3. Personalizar metadatos, autor y fechas.
4. Registrar el proyecto en el catálogo raíz `CONTEXT.md`.

---

## 📂 Estructura del Repositorio

```text
proyectosML/
├── AGENTS.md                              # Directrices canónicas del espacio Umbrella
├── CLAUDE.md                              # Adaptador para Claude Code
├── .cursorrules                           # Adaptador para Cursor IDE
├── .windsurfrules                         # Adaptador para Windsurf / Cascade
├── .github/copilot-instructions.md        # Adaptador para GitHub Copilot
├── CONTEXT.md                             # Catálogo de proyectos activos
├── README.md                              # Esta guía
├── SETUP_GUIDE.md                         # Guía de recuperación paso a paso para nuevo equipo
├── bootstrap.sh                           # Instalador universal en 1 clic
├── init-project.sh                        # Generador de proyectos
├── .gitignore                             # Filtros globales para DS/ML/Agents
│
├── _baseline/                             # La Fábrica (reproducible y portable)
│   ├── global_config/GEMINI.md            # Reglas universales para Antigravity
│   ├── skills/
│   │   ├── icm-architect/                 # Skill de RinDig para diseño y auditoría
│   │   └── project-scaffold/              # Skill nativa para crear proyectos por chat
│   └── _templates/                        # Plantillas maestras con soporte multi-IA
│       ├── ds-project-scaffold/           # Plantilla Ciencia de Datos (con research/)
│       ├── ml-project-scaffold/           # Plantilla ML Productivo
│       └── agentic-project-scaffold/      # Plantilla Desarrollo Agéntico
│
└── projects/                              # Los Productos (tus proyectos de trabajo)
    └── (proyectos creados con init-project.sh)
```

---

## 🧠 La Carpeta `research/` en Proyectos de Ciencia de Datos

En cada proyecto de Ciencia de Datos (`--type ds`), la carpeta `research/` proporciona el anclaje científico y teórico necesario:
- `01_problem_formulation.md`: Formulación matemática formal, espacios de variables y funciones de pérdida.
- `02_literature_review.md`: Estado del arte, papers revisados y síntesis de metodologías.
- `03_methodological_rationale.md`: Justificación técnica de decisiones de diseño (algoritmo, métrica, split).
- `notes/hypothesis_log.md`: Bitácora de pensamiento y validación de hipótesis (asistidas por IA o manuales).
- `references/`: Bibliografía y enlaces a fuentes formales.

## 🤝 Autor y Licencia

- **Autor**: [Felipe Marchant](https://github.com/f-marchant)
- **Linkedin**: [felipemarchant](linkedin.com/in/felipemarchant)
- **Licencia**: MIT


## 📚 Reconocimientos y Fuentes

Este repositorio implementa y extiende las siguientes metodologías y herramientas de código abierto:

- **[Interpretable Context Methodology (ICM)](https://github.com/RinDig/Interpretable-Context-Methodology)** por RinDig (Licencia MIT).
  - *Base conceptual*: Sustitución de orquestadores complejos por estructura de sistema de archivos, contratos de etapa y disciplina de tokens.
- **[icm-architect](https://github.com/RinDig/icm-architect)** por RinDig (Licencia MIT).
  - *Skill integrada*: Diseñador y auditor de workspaces en los 6 arquetipos formales.
- **[Cookiecutter Data Science](https://github.com/drivendata/cookiecutter-data-science)** por DrivenData (Licencia BSD-3-Clause).
  - *Estructura modular de datos por capas (`data/raw`, `data/interim`, `data/processed`)*.
