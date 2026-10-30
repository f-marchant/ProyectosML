---
name: handoff
description: Compacta la conversación actual en un documento de transferencia estructurado para que otra sesión o agente continúe sin perder contexto ni sobrecargar la ventana de tokens. Úsalo al cerrar sesión, rotar tareas o preparar un traspaso.
---

# Handoff — Traspaso y Compresión de Contexto

Esta skill resume y compacta el estado de trabajo de la sesión actual para permitir una continuidad limpia en una sesión posterior o en un nuevo agente, manteniendo la disciplina del presupuesto de contexto (2.000–8.000 tokens).

## Instrucciones

1. **Destino del Artefacto**:
   - Genera un documento markdown de transferencia (`HANDOFF.md` en el directorio de trabajo actual, o en el directorio temporal si se trata de una nota efímera).
2. **Contenido Esencial**:
   - **Objetivo Central**: Qué se buscaba lograr en esta sesión.
   - **Estado Actual**: Qué se completó, qué quedó en progreso y qué está bloqueado.
   - **Decisiones Técnicas Tomadas**: Decisiones de diseño, arquitectura o parámetros definidos con el usuario.
   - **Punteros a Archivos Relevantes**: Enlaces directos a archivos modificados, contratos `CONTEXT.md` o salidas intermedias (¡no dupliques código completo en el handoff, solo referencias!).
   - **Skills Sugeridas para el Siguiente Agente**: Indica explícitamente qué skills o herramientas debería invocar la próxima sesión (ej. `diagnose`, `icm-architect`, `project-scaffold`, etc.).
   - **Próximos Pasos Inmediatos**: Lista priorizada y ejecutable de las siguientes 2–3 acciones concretas.
3. **Seguridad y Redacción**:
   - Redacta tokens, credenciales o claves privadas (`<REDACTED>`).
4. **Si el usuario especificó argumentos o indicaciones adicionales**:
   - Adapta el resumen enfocándolo hacia el objetivo de la próxima sesión señalado por el usuario.
