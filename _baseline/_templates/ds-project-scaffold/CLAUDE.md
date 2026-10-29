# CLAUDE.md — {{PROJECT_NAME}} (Data Science)

> **Tipo**: Ciencia de Datos / Análisis Predictivo  
> **Objetivo**: {{PROJECT_DESCRIPTION}}

## Reglas y Metodología (ICM)
- **Línea Base y Restricciones**: Consulta [AGENTS.md](AGENTS.md).
- **Contratos de Etapa**: Consulta [CONTEXT.md](CONTEXT.md).
- **Sustento Teórico**: Consulta `research/` (`01_problem_formulation.md`, `03_methodological_rationale.md`).
- **Diccionario de Datos**: Consulta `_context/domain.md`.
- **Estrategia Estadística**: Consulta `_context/conventions.md` (`seed=42`, CV temporal o estratificado).

## Reglas Críticas
1. `data/raw/` es de solo lectura.
2. Nunca filtrar datos de validación/test en el entrenamiento (No Data Leakage).
3. No leer datasets masivos directamente; consulta `_context/domain.md`.
