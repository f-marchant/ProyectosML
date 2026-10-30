---
name: implement-spec
description: Ejecuta la implementación de especificaciones descompuestas en tickets mediante subagentes concurrentes o secuenciales según el grafo de dependencias. Úsalo para orquestar la construcción de tickets desbloqueados.
---

# Implement-Spec — Orquestación de Implementación de Tickets

Esta skill toma el grafo de tickets generados por `/to-tickets` y coordina su implementación ejecutando la **frontera de trabajo** (aquellos tickets cuyos bloqueos están resueltos).

## Principios de Ejecución

1. **Ventana Limpia por Subagente**: Cada ticket se implementa idealmente con una ventana de contexto limpia para evitar arrastrar residuos de memoria anteriores.
2. **Comunicación por Punteros**: Comunica a los subagentes únicamente los punteros hacia la especificación, el ticket asignado y los contratos relevantes, sin volcar archivos enteros.
3. **Avance de la Frontera**: Al completarse un ticket y verificarse sus criterios de aceptación, los tickets dependientes quedan desbloqueados y pasan a la frontera de ejecución.

## Flujo de Trabajo

1. **Calcular la Frontera Inicial**: Identifica todos los tickets con `Bloqueado por: Ninguno`.
2. **Ejecutar Ticket a Ticket**:
   - Asigna el ticket al subagente o procésalo en el entorno actual.
   - Aplica pruebas/evals locales para confirmar que cumple los criterios de aceptación.
3. **Integración y Validación**:
   - Integra los cambios al branch o módulo correspondiente.
   - Ejecuta los tests o evals de regresión para garantizar que nada previo se rompió.
4. **Actualizar el Estado**:
   - Marca el ticket como completado.
   - Recalcula la frontera e inicia los siguientes tickets desbloqueados hasta agotar el grafo.
