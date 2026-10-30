---
name: retro
description: Realiza una retrospectiva estructurada sobre una sesión de desarrollo para identificar fricciones, optimizar el uso de herramientas y mejorar las reglas en AGENTS.md y guardarraíles del repositorio. Úsalo cuando el usuario pida una 'retro', 'retrospectiva' o analizar fallos de un agente.
---

# Retro — Retrospectiva y Mejora Continua de Agentes

El objetivo de esta retrospectiva es analizar la sesión de trabajo y proponer mejoras concretas en el **entorno del agente** (reglas, herramientas, linters y documentación) para que las futuras iteraciones sean más rápidas, precisas y token-eficientes.

## Pasos

1. **Revisar las Fuentes Primarias**:
   - Analiza el historial de la sesión actual, los diffs de código y los comandos ejecutados.
   - Identifica momentos de fricción: comandos fallidos reiterados, búsquedas excesivas de archivos o correcciones manuales del usuario.

2. **Categorías de Análisis**:
   - **Navegación y Descubrimiento**: ¿Le costó trabajo al agente ubicar los archivos correctos? ¿Hacen falta punteros explícitos en `CONTEXT.md` o `AGENTS.md`?
   - **Guardarraíles Automatizados**: ¿Cometió el agente errores que un linter (Ruff, Flake8), test o validación pre-commit podría haber atrapado automáticamente? *Prioridad: Es preferible un check determinista automático antes que una nueva regla en texto plano.*
   - **Estándares de Código y Directrices**: ¿Falló una convención de nombres, tipado o manejo de datos? Proponer aclaraciones concisas en las directrices del proyecto.
   - **Economía de Herramientas y Tokens**: ¿Se hicieron llamadas a herramientas innecesariamente costosas? ¿Se intentó leer archivos binarios o datasets completos violando la regla de 2k-8k tokens?
   - **Instrucciones Muertas (No-ops)**: ¿Hay reglas en `AGENTS.md` o `.windsurfrules` / `.cursorrules` redundantes que no alteran el comportamiento pero consumen tokens en cada turno?
   - **Acceso a la Información**: ¿Faltaba información de entorno, variables o documentación de librerías requeridas?

3. **Presentar las Propuestas de Mejora**:
   - Organiza los hallazgos en orden de impacto y severidad.
   - Para cada hallazgo, proporciona el cambio exacto a realizar (ej. adición a un linter, ajuste en `AGENTS.md` o nuevo test de higiene).
