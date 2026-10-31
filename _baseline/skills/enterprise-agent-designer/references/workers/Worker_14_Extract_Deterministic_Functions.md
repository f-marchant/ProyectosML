# WORKER 14: Extract_Deterministic_Functions

**Versión**: 7.3.0

Contrato (INPUTS y OUTPUTS) definido en `SKILL.md`, sección 10, WORKER 14.
Este archivo contiene el método paso a paso. Cargar solo cuando el WORKER
esté activo según la sección 9.1 del `SKILL.md`.

**Objetivo**:
Extraer operaciones exactas fuera del razonamiento generativo.

[SEQUENTIAL_BLOCK]

1. Identificar cálculos.
2. Identificar normalizaciones.
3. Identificar comparaciones de umbrales.
4. Identificar conciliaciones.
5. Identificar validaciones de esquema.
6. Definir contrato por función.
7. Definir inputs y tipos.
8. Definir outputs y tipos.
9. Definir errores.
10. Definir precisión.
11. Definir redondeo.
12. Definir casos límite.
13. Seleccionar flow, connector, API, function o script.
14. Exigir mismo input, mismo output.
15. Exigir versionado.
16. Prohibir que el LLM sustituya una función disponible.
17. Prohibir operaciones matemáticas críticas mediante texto libre.

[END_SEQUENTIAL_BLOCK]
