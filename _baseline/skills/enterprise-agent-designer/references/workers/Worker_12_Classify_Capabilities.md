# WORKER 12: Classify_Capabilities

**Versión**: 7.3.0

Contrato (INPUTS y OUTPUTS) definido en `SKILL.md`, sección 10, WORKER 12.
Este archivo contiene el método paso a paso. Cargar solo cuando el WORKER
esté activo según la sección 9.1 del `SKILL.md`.

**Objetivo**:
Clasificar las funciones del agente y seleccionar su implementación.

[SEQUENTIAL_BLOCK]

1. Identificar tareas semánticas.
2. Identificar tareas simbólicas.
3. Identificar tareas deterministas.
4. Identificar tareas generativas.
5. Identificar tareas de orquestación.
6. Identificar tareas de validación.
7. Clasificar cada capability.
8. Seleccionar ImplementationType.
9. Definir inputs.
10. Definir outputs.
11. Definir autoridad.
12. Definir referencias.
13. Definir validaciones.
14. Prohibir cálculo libre por el modelo.
15. Prohibir skills para operaciones puramente deterministas cuando exista
    una función más apropiada.
16. Registrar fallback de plataforma.

[END_SEQUENTIAL_BLOCK]
