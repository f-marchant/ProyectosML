# AGENTS.md — {{PROJECT_NAME}} (Data Science)

> **Tipo de Proyecto**: Ciencia de Datos / Análisis Predictivo
> **Objetivo**: {{PROJECT_DESCRIPTION}}
> **Fecha de Creación**: {{CREATION_DATE}}

---

## 1. Dónde estoy y Qué rige
Estás en el proyecto de Ciencia de Datos `{{PROJECT_NAME}}`. Sigue la metodología ICM:
- **Línea base global**: Respeta las reglas universales en `~/.gemini/config/GEMINI.md`.
- **Sustento teórico**: Consulta `research/` antes de implementar algoritmos o funciones de pérdida.
- **Diccionario de datos**: Consulta `_context/domain.md` para conocer las variables y su significado.
- **Ruta de etapas**: Consulta `CONTEXT.md` para saber en qué etapa se encuentra el proyecto.

---

## 2. Restricciones Técnicas Inviolables
1. **Inmutabilidad**: `data/raw/` es solo lectura. Guarda datos limpios en `data/processed/`.
2. **Data Leakage**: Nunca apliques transformaciones sobre el conjunto total de datos. Ajusta en `train` y transforma en `val`/`test`.
3. **Reproducibilidad**: Fija siempre semillas aleatorias (`seed=42`).
4. **Contexto Limpio**: No leas datasets enteros (`.csv`, `.parquet`). Lee `_context/domain.md` o pide una muestra de 5 filas si es necesario.

---

## 3. Comandos Rápidos
- Correr tests: `pytest tests/`
- Formatear código: `ruff format src/`
- Linting: `ruff check src/`
