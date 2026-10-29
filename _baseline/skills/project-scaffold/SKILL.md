---
name: project-scaffold
description: >-
  Inicializa y estandariza nuevos proyectos en el espacio de trabajo proyectosML
  siguiendo la metodología ICM (Interpretable Context Methodology) para Ciencia de Datos (ds),
  Machine Learning productivo (ml) o Desarrollo Agéntico (agentic).
  Úsalo cuando el usuario pida: "crea un nuevo proyecto", "inicializa un proyecto",
  "scaffold a project", "nuevo proyecto de data science", "nuevo proyecto agéntico" o similar.
---

# Project Scaffold (proyectosML)

Este skill permite instanciar nuevos proyectos perfectamente estandarizados dentro de `/home/fmarchant/proyectosML/projects/` usando las plantillas de `_baseline/_templates/`.

## Tipos de Proyectos Disponibles

1. **`ds` (Ciencia de Datos)**:
   - Para: Análisis exploratorio, formulación matemática/teórica, hipótesis, modelos predictivos, y reportes analíticos.
   - Incluye: `research/` (sustento teórico, estado del arte), `data/` (raw inmutable, interim, processed), `notebooks/` cronológicos, `src/` modular, `reports/`.

2. **`ml` (Machine Learning Productivo)**:
   - Para: Modelos productivos, pipelines de entrenamiento automatizado, APIs con FastAPI y despliegue en contenedores.
   - Incluye: `src/api/`, `src/pipeline/`, `src/inference/`, `tests/` unit/integration, `Dockerfile`, exportación de modelos.

3. **`agentic` (Desarrollo Agéntico)**:
   - Para: Asistentes autónomos, sistemas multi-agente, integración con tools/MCP, RAG y evaluación de comportamiento.
   - Incluye: `prompts/`, `tools/` (JSON schemas + implementación), `evals/` (golden datasets, judge rubrics), `memory/`, `logs/traces/`.

---

## Procedimiento de Inicialización

El agente puede ejecutar el script CLI directamente o seguir estos pasos:

### Método A: Usando el script automatizado (Recomendado)

```bash
cd /home/fmarchant/proyectosML
./init-project.sh <nombre-proyecto> --type <ds|ml|agentic> "<descripción opcional>"
```

### Método B: Ejecución manual paso a paso

1. **Validación de nombre**:
   Verificar que no exista `/home/fmarchant/proyectosML/projects/<nombre-proyecto>`. El nombre debe ser en minúsculas con guiones medios (kebab-case).

2. **Copia de plantilla**:
   - Para `ds`: Copiar `_baseline/_templates/ds-project-scaffold/` a `projects/<nombre-proyecto>/`.
   - Para `ml`: Copiar `_baseline/_templates/ml-project-scaffold/` a `projects/<nombre-proyecto>/`.
   - Para `agentic`: Copiar `_baseline/_templates/agentic-project-scaffold/` a `projects/<nombre-proyecto>/`.

3. **Personalización de Metadatos**:
   Actualizar los placeholders en `AGENTS.md` y `CONTEXT.md` del nuevo proyecto con el nombre, fecha y objetivo del usuario.

4. **Registro en el Catálogo Raíz**:
   Agregar una entrada en `/home/fmarchant/proyectosML/CONTEXT.md` en la tabla de proyectos activos.

5. **Alineación de Contexto**:
   Preguntar al usuario si desea completar el archivo `_context/domain.md` (o `research/01_problem_formulation.md`) para definir el objetivo antes de comenzar a programar.
