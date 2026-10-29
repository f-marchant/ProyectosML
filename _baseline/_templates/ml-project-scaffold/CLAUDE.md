# CLAUDE.md — {{PROJECT_NAME}} (ML Productivo / MLOps)

> **Tipo**: Machine Learning Productivo / API / Inferencia  
> **Objetivo**: {{PROJECT_DESCRIPTION}}

## Reglas y Metodología (ICM)
- **Línea Base y Restricciones**: Consulta [AGENTS.md](AGENTS.md).
- **Contratos y Arquitectura**: Consulta [CONTEXT.md](CONTEXT.md).
- **Especificaciones de API**: Consulta `_context/api_specs.md`.
- **Pipeline de Datos**: Consulta `_context/architecture.md`.

## Reglas Críticas
1. Todo payload de entrada/salida debe validarse con Pydantic.
2. Toda lógica de negocio debe residir en `src/` (no notebooks en producción).
3. Escribir tests en `tests/` para cada endpoint y transformación.
