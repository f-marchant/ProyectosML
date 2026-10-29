# AGENTS.md — {{PROJECT_NAME}} (ML Productivo / MLOps)

> **Tipo de Proyecto**: Machine Learning Productivo / API / Inferencia
> **Objetivo**: {{PROJECT_DESCRIPTION}}
> **Fecha de Creación**: {{CREATION_DATE}}

---

## 1. Dónde estoy y Qué rige
Estás en el proyecto de Machine Learning productivo `{{PROJECT_NAME}}`. Sigue la metodología ICM:
- **Línea base global**: Respeta `~/.gemini/config/GEMINI.md`.
- **Contratos de API**: Consulta `_context/api_specs.md` para endpoints y payloads Pydantic.
- **Pipeline de Datos**: Consulta `_context/architecture.md` para el flujo de reentrenamiento e inferencia.

---

## 2. Restricciones Técnicas Inviolables
1. **Validación de Schemas**: Todo dato de entrada/salida a la API debe estar validado con Pydantic.
2. **Sin Notebooks en Producción**: La lógica de negocio y entrenamiento debe residir exclusivamente en `src/`.
3. **Tests Obligatorios**: Todo endpoint y función de transformación debe tener tests en `tests/`.
4. **Contenerización**: La aplicación debe empaquetarse limpiamente con `Dockerfile`.

---

## 3. Comandos Rápidos
- Ejecutar API local: `uvicorn src.api.main:app --reload --port 8000`
- Ejecutar Pipeline: `python -m src.pipeline.train`
- Correr tests: `pytest tests/`
- Linting y formato: `ruff check src/ && ruff format src/`
