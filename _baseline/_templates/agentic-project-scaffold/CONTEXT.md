# CONTEXT.md — Arquitectura Agéntica y Contratos: {{PROJECT_NAME}}

Este archivo define el flujo de razonamiento y los componentes del sistema agéntico.

---

## 1. Mapa de Contexto

| Carpeta / Archivo | Tipo de Información | Cuándo consultarlo |
| :--- | :--- | :--- |
| `_context/persona.md` | Personalidad, rol, tono y límites del agente | Al ajustar comportamiento |
| `_context/safety_guardrails.md` | Políticas de seguridad y fallbacks | Al validar llamadas y permisos |
| `prompts/system_prompts/` | System prompts versionados | Al modificar directrices del agente |
| `prompts/templates/` | Plantillas parametrizadas con variables | Al formatear entradas de usuario |
| `tools/definitions/` | Esquemas JSON de herramientas y parámetros | Al registrar nuevas capacidades |
| `tools/implementations/` | Código ejecutable de las tools | Al desarrollar la lógica de herramientas |
| `memory/` | Sesiones y base de vectores para RAG | Al gestionar estado y contexto persistente |
| `evals/` | Golden datasets y rúbricas de evaluación | Al medir precisión y evitar regresiones |
| `src/` | Bucle de ejecución (ReAct / Graph) | Al orquestar el flujo de decisiones |

---

## 2. Flujo de Ejecución Agéntica
1. **Entrada de Usuario**: Se valida contra `_context/safety_guardrails.md`.
2. **Inyección de Prompt**: Se ensambla `prompts/system_prompts/` con el historial en `memory/`.
3. **Bucle de Invocación**: El modelo decide si responder o emitir llamadas a `tools/definitions/`.
4. **Ejecución y Feedback**: `tools/implementations/` ejecuta la acción y devuelve el resultado al contexto.
5. **Registro**: Se guardan tokens y latencia en `logs/traces/`.
