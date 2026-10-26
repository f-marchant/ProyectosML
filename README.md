# proyectosML — Línea Base y Espacio de Trabajo con ICM para Antigravity

[![Metodología: ICM](https://img.shields.io/badge/Methodology-ICM-blue.svg)](https://github.com/RinDig/Interpretable-Context-Methodology)
[![AI Assistant: Antigravity](https://img.shields.io/badge/Agent-Google_Antigravity-orange.svg)](https://antigravity.google)
[![Licencia: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Espacio de trabajo unificado basado en el patrón **Umbrella** de **Interpretable Context Methodology (ICM)** para gestionar proyectos de **Ciencia de Datos**, **Machine Learning Productivo** y **Desarrollo Agéntico** con la misma línea base de ingeniería, reproducibilidad y disciplina de contexto.

---

## 🌟 Características Principales

1. **Línea Base Unificada (Patrón Umbrella)**:
   - Configuración global para Antigravity en `_baseline/global_config/GEMINI.md`.
   - Incorporación nativa de la skill [`icm-architect`](https://github.com/RinDig/icm-architect) para diseñar y auditar workspaces.
   - Aislamiento total entre proyectos: cero contaminación cruzada de dependencias o contexto.
2. **Tres Arquetipos de Proyectos Especializados**:
   - 🔬 **Ciencia de Datos (`ds`)**: Capas de datos (`raw/`, `interim/`, `processed/`), notebooks cronológicos, código modular y carpeta dedicada **`research/`** para formulación matemática y estado del arte.
   - ⚙️ **Machine Learning Productivo (`ml`)**: Pipelines de reentrenamiento, servicio web con FastAPI, validación con Pydantic, tests unitarios/integración y `Dockerfile`.
   - 🤖 **Desarrollo Agéntico (`agentic`)**: Gestión de `prompts/`, catálogo de `tools/` (JSON schemas + implementación), banco de `evals/`, memoria y trazas de observabilidad.
3. **Automatización en 1 Comando**:
   - `init-project.sh`: Script CLI para instanciar cualquier proyecto con su contrato de contexto completo en 2 segundos.
4. **Portabilidad y Respaldo Total**:
   - `bootstrap.sh`: Configura Antigravity en cualquier máquina personal nueva en menos de 1 minuto.

---

## 🚀 Inicio Rápido

### 1. Inicializar la Línea Base en tu Máquina
Si acabas de clonar este repositorio en una máquina nueva:
```bash
cd ~/proyectosML
./bootstrap.sh
```
El script vinculará automáticamente las reglas y skills a tu configuración global de Antigravity (`~/.gemini/config/`).

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
2. Personalizar metadatos, autor y fechas.
3. Registrar el proyecto en el catálogo raíz `CONTEXT.md`.

---

## 📂 Estructura del Repositorio

```text
proyectosML/
├── AGENTS.md                              # Directrices del espacio Umbrella
├── CONTEXT.md                             # Catálogo de proyectos activos
├── README.md                              # Esta guía
├── SETUP_GUIDE.md                         # Guía de recuperación paso a paso para nuevo equipo
├── bootstrap.sh                           # Instalador en 1 clic
├── init-project.sh                        # Generador de proyectos
├── .gitignore                             # Filtros globales para DS/ML/Agents
│
├── _baseline/                             # La Fábrica (reproducible y portable)
│   ├── global_config/GEMINI.md            # Reglas universales para Antigravity
│   ├── skills/
│   │   ├── icm-architect/                 # Skill de RinDig para diseño y auditoría
│   │   └── project-scaffold/              # Skill nativa para crear proyectos por chat
│   └── _templates/                        # Plantillas maestras
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

---

## 🛡️ Principios Inviolables de Git Hygiene

Este repositorio está configurado para **proteger tus datos y modelos**:
- Datasets pesados (`*.csv`, `*.parquet`, `data/raw/*`) y pesos entrenados (`*.pkl`, `*.pt`, `*.onnx`) están **excluidos del control de versiones**.
- Las credenciales (`.env`, `credentials.json`) nunca se subirán a GitHub.
- El repositorio en GitHub preserva la **arquitectura, código, contratos de contexto y documentación**, manteniéndose ligero y seguro.

---

## 🤝 Autor y Licencia

- **Autor**: [Felipe Marchant](https://github.com/f-marchant)
- **Licencia**: MIT
