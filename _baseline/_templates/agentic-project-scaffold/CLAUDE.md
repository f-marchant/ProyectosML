# CLAUDE.md — {{PROJECT_NAME}} (Desarrollo Agéntico)

> **Tipo**: Sistema Agéntico Autónomo / Orquestación / LLM Engineering  
> **Objetivo**: {{PROJECT_DESCRIPTION}}

## Reglas y Metodología (ICM)
- **Línea Base y Restricciones**: Consulta [AGENTS.md](AGENTS.md).
- **Contratos y Flujo**: Consulta [CONTEXT.md](CONTEXT.md).
- **Persona del Agente**: Consulta `_context/persona.md`.
- **Seguridad y Guardrails**: Consulta `_context/safety_guardrails.md`.

## Reglas Críticas
1. Los prompts nunca deben hardcodearse en código; residen en `prompts/`.
2. Las herramientas requieren esquema tipado en `tools/definitions/`.
3. Validar cambios contra los benchmarks en `evals/`.
