# WORKER 06: Stabilize_Baseline

**Versión**: 7.3.0

Contrato (INPUTS y OUTPUTS) definido en `SKILL.md`, sección 10, WORKER 06.
Este archivo contiene el método paso a paso. Cargar solo cuando el WORKER
esté activo según la sección 9.1 del `SKILL.md`.

**Objetivo**:
Proponer la corrección de inconsistencias críticas antes de migrar o
reestructurar.

[SEQUENTIAL_BLOCK]

1. Canonicalizar nombres.
2. Corregir propuestas de INPUTS y OUTPUTS.
3. Corregir propuestas de tipos y ENUM.
4. Corregir intervalos.
5. Definir precedencia de decisiones.
6. Identificar resultados que no deben sobrescribirse.
7. Conciliar contratos.
8. Identificar reglas duplicadas.
9. Proponer correcciones mínimas.
10. Mantener compatibilidad cuando sea posible.
11. Marcar como críticos los problemas que bloquean la migración.
12. No modificar reglas de negocio sin autorización.
13. Determinar baseline_status.
14. Detener el diseño productivo si quedan hallazgos críticos no resueltos.

[END_SEQUENTIAL_BLOCK]
