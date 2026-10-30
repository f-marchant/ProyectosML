---
name: grill-me
description: Entrevista exhaustiva y estructurada para desafiar y pulir un plan, diseño técnico o arquitectura antes de programar. Usa esta skill cuando el usuario quiera someter a prueba sus ideas o mencione 'grill-me', 'entrevístame' o 'desafía mi plan'.
---

# Grill-Me — Stress-Testing de Decisiones y Arquitectura

Entrevista al usuario sistemáticamente hasta alcanzar un entendimiento compartido y sin ambigüedades. Modela las decisiones como un **árbol de diseño**: cada decisión técnica o de negocio ramifica en las sub-decisiones que dependen de ella.

## Metodología por Rondas

Trabaja el árbol en **rondas**. La **frontera** está compuesta por aquellas decisiones cuyos prerrequisitos ya están resueltos (las preguntas que puedes formular *ahora* sin adivinar respuestas que aún no conoces).

Formula toda la frontera en una sola ronda: enumera cada pregunta y proporciona siempre tu **respuesta recomendada**. Luego espera las respuestas del usuario antes de pasar a la siguiente ronda.

### Formato de cada Ronda

```markdown
❓ **Q1** - **<Título de la decisión>**: <Cuerpo de la pregunta, contexto y opciones consideradas>

➡️ **Recomendación**: <Tu propuesta técnica fundamentada y directa>

---

❓ **Q2** - **<Título de la decisión>**: <Cuerpo de la pregunta, contexto y opciones consideradas>

➡️ **Recomendación**: <Tu propuesta técnica fundamentada y directa>
```

Formula cada pregunta de modo que un simple *"Sí"* o *"De acuerdo"* acepte tu respuesta recomendada por defecto.

## Reglas de Ejecución

1. **La búsqueda de hechos es tu trabajo, nunca del usuario**:
   - Si una pregunta de la frontera requiere datos del entorno (inspeccionar el sistema de archivos, configuraciones existentes, esquemas de tablas o código base), investígalo tú mismo mediante tus herramientas antes de preguntar.
   - Nunca le preguntes al usuario algo que puedas verificar directamente en el código o repositorio.
2. **Las decisiones le corresponden al usuario**:
   - Plantea los trade-offs de forma transparente (costo, latencia, complejidad, deuda técnica).
3. **Avance de la Frontera**:
   - Cada respuesta del usuario reconfigura el árbol: las decisiones zanjadas empujan la frontera hacia afuera y desbloquean las preguntas dependientes.
   - Una pregunta cuya respuesta depende de otra pregunta abierta en esta ronda pertenece a una ronda *posterior*.
4. **Criterio de Término**:
   - La sesión concluye cuando la frontera está vacía: todas las ramas del diseño han sido visitadas y no queda ningún supuesto implícito sin validar.
   - No comiences a escribir código ni a alterar el sistema hasta que el usuario confirme que se ha llegado al entendimiento compartido.
