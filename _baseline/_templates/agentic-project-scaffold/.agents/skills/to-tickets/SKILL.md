---
name: to-tickets
description: Descompone una especificación técnica o plan en tickets verticales autónomos (tracer bullets) con dependencias explícitas (grafo de bloqueos). Úsalo cuando una especificación esté lista para dividirse en tareas ejecutables por agentes.
---

# To-Tickets — Partición en Tareas Verticales y Grafo de Bloqueos

Descompone una especificación técnica o plan en **tickets ejecutables** organizados como rebanadas verticales (tracer bullets), declarando explícitamente qué tickets **bloquean** a cuáles.

## Reglas de Partición Vertical

1. **Rebanadas Verticales**: Cada ticket debe atravesar de extremo a extremo las capas necesarias (schema -> tool/función -> prompt -> eval/test) en lugar de crear tickets horizontales monolíticos.
2. **Autonomía y Verificabilidad**: Cada ticket completado debe poder probarse y validarse por sí mismo.
3. **Tamaño Acotado**: Cada ticket debe diseñarse para caber holgadamente dentro de una ventana de contexto limpia (presupuesto de 2k-8k tokens).
4. **Declaración Explícita de Bloqueos**: Cada ticket debe indicar `Bloqueado por: [IDs de tickets]` o `Ninguno (puede iniciar de inmediato)`.

## Proceso

1. **Revisar la Especificación**: Lee el documento de especificación técnica generado previamente.
2. **Proponer la Lista de Tickets**: Muestra al usuario la partición inicial indicando:
   - **ID y Título**: Breve y descriptivo.
   - **Bloqueado por**: Dependencias previas necesarias.
   - **Qué entrega**: El comportamiento verificable que implementa.
3. **Validar con el Usuario**: Ajusta granularidad, dependencias o fusiones solicitadas por el usuario.
4. **Emitir los Tickets**: Guarda cada ticket individualmente (por ejemplo en `docs/tickets/` o `.scratch/tickets/` con la nomenclatura `NN-<slug>.md`).

### Formato de Ticket

```markdown
# [ID]: [Título del Ticket]

**Qué construir:**
Descripción del comportamiento de extremo a extremo que este ticket habilita.

**Bloqueado por:**
[Lista de IDs de tickets previos] o "Ninguno (listo para comenzar inmediatamente)"

**Criterios de Aceptación:**
- [ ] Criterio 1
- [ ] Criterio 2
- [ ] Criterio de prueba/evaluación pasando
```
