# CLAUDE.md — proyectosML (Umbrella Workspace)

> Este espacio de trabajo opera bajo la metodología **Interpretable Context Methodology (ICM)**.

## Enrutamiento y Principios
- **Reglas Principales y Filosofía**: Consulta [AGENTS.md](AGENTS.md).
- **Catálogo de Proyectos Activos**: Consulta [CONTEXT.md](CONTEXT.md).
- **Creación de Nuevos Proyectos**: Ejecuta `./init-project.sh <nombre> --type <ds|ml|agentic>`.
- **Fábrica de Estándares**: Carpeta `_baseline/` con plantillas y skills (`icm-architect`, `project-scaffold`).

## Disciplina de Contexto
- Presupuesto de 2.000 a 8.000 tokens por interacción.
- Cuando trabajes en un subproyecto dentro de `projects/<nombre>/`, respeta sus contratos locales en `CONTEXT.md` y `_context/`.
