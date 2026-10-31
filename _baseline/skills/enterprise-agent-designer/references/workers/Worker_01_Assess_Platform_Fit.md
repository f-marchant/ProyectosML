# WORKER 01: Assess_Platform_Fit

**Versión**: 7.3.0

Contrato (INPUTS y OUTPUTS) definido en `SKILL.md`, sección 10, WORKER 01.
Este archivo contiene el método paso a paso. Cargar solo cuando el WORKER
esté activo según la sección 9.1 del `SKILL.md`.

**Objetivo**:
Determinar qué componentes pueden implementarse en Agent Builder y cuáles
requieren Copilot Studio, custom skills, tools, flows o servicios externos.

[SEQUENTIAL_BLOCK]

1. Identificar la plataforma prevista.
2. Identificar si se dispone de Agent Builder.
3. Identificar si se dispone de Copilot Studio.
4. Verificar si las custom skills están disponibles.
5. Verificar restricciones de Information Barriers.
6. Verificar necesidades de acciones externas.
7. Verificar necesidades de conectores o workflows.
8. Verificar necesidades de cálculo determinista.
9. Verificar sensibilidad y requisitos de cumplimiento.
10. Clasificar preliminarmente cada necesidad por ImplementationType.
11. Recomendar Agent Builder cuando el escenario sea declarativo.
12. Recomendar Copilot Studio cuando se requieran acciones, flows o
    conectores.
13. Recomendar implementación pro-code cuando se requieran garantías o
    integraciones no cubiertas por low-code.
14. Registrar capacidades no verificadas.
15. No asumir licencias ni previews no confirmadas.

[END_SEQUENTIAL_BLOCK]
