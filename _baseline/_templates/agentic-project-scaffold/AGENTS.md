# AGENTS.md — {{PROJECT_NAME}} (Desarrollo Agéntico)

> **Tipo de Proyecto**: Sistema Agéntico Autónomo / Orquestación / LLM Engineering
> **Objetivo**: {{PROJECT_DESCRIPTION}}
> **Fecha de Creación**: {{CREATION_DATE}}

---

## 1. Dónde estoy y Qué rige
Estás en el proyecto de desarrollo agéntico `{{PROJECT_NAME}}`. Sigue la metodología ICM:
- **Línea base global**: Respeta `~/.gemini/config/GEMINI.md`.
- **Persona del Agente**: Consulta `_context/persona.md` para rol, tono y límites.
- **Guardrails y Seguridad**: Consulta `_context/safety_guardrails.md` para evitar inyecciones de prompts y acciones de riesgo.

---

## 2. Restricciones Técnicas Inviolables
1. **Separación Prompts vs. Código**: Los prompts nunca se escriben en línea dentro del código Python; deben residir en `prompts/`.
2. **Definición Estricta de Herramientas**: Toda tool debe tener esquema tipado (Pydantic / JSON Schema) en `tools/definitions/`.
3. **Evals antes de Despliegue**: Ningún cambio de prompt o arquitectura se valida sin correr el benchmark en `evals/`.
4. **Trazabilidad**: Toda llamada a LLM debe registrar tokens y latencia en `logs/traces/`.

---

## 3. Comandos Rápidos
- Correr agente: `python -m src.agent`
- Ejecutar suite de Evals: `pytest evals/`
- Linting y formato: `ruff check src/ && ruff format src/`
