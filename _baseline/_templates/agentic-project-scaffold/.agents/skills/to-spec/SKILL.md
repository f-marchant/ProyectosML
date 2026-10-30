---
name: to-spec
description: Sintetiza la conversación y el diseño actual en una especificación técnica formal y estructurada sin realizar nuevas entrevistas. Úsalo al cerrar la fase de diseño para formalizar requerimientos y contratos antes de la partición de tareas.
---

# To-Spec — Síntesis de Especificación Técnica

Esta skill toma el contexto acordado en la conversación y el estado actual del repositorio para producir una especificación técnica completa y formal. **No entrevistes al usuario nuevamente**: sintetiza lo que ya se discutió y acordó.

## Proceso

1. **Explorar el entorno**: Revisa los contratos de contexto existentes (`CONTEXT.md`, `_context/domain.md` o herramientas disponibles). Usa el vocabulario del proyecto.
2. **Definir junturas de prueba (Seams)**: Identifica los puntos clave de integración y pruebas (evals, aserciones, interfaces de entrada/salida).
3. **Redactar la Especificación**: Genera el documento (típicamente en `research/spec.md` o `docs/spec.md`) usando la siguiente estructura:

### Estructura de la Especificación

```markdown
# Spec: [Nombre de la Funcionalidad o Flujo Agéntico]

## 1. Declaración del Problema (Problem Statement)
El problema concreto y medible que se está abordando desde la perspectiva del usuario o del sistema.

## 2. Solución Propuesta (Proposed Solution)
Resumen de la arquitectura o solución desde la perspectiva del usuario o consumidor.

## 3. Historias de Usuario / Casos de Uso Agénticos (Stories)
Lista numerada de casos de uso bajo el formato:
- Como [rol/agente], quiero [acción o capacidad], para [beneficio esperado].

## 4. Decisiones de Implementación (Implementation Decisions)
- Módulos, herramientas (MCP) o agentes a crear/modificar.
- Esquemas de datos (schemas), contratos de entrada/salida y estado.
- Manejo de memoria, observabilidad y manejo de excepciones.

## 5. Decisiones de Evaluación y Pruebas (Testing & Evals)
- Métricas o rúbricas de evaluación (evals).
- Datasets dorados (golden datasets) de prueba.
- Pruebas de integración para tools y MCP servers.

## 6. Fuera de Alcance (Out of Scope)
Lo que explícitamente NO se cubrirá en esta iteración.
```
