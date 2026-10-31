# WORKER 05: Detect_Inconsistencies

**Versión**: 7.3.0

Contrato (INPUTS y OUTPUTS) definido en `SKILL.md`, sección 10, WORKER 05.
Este archivo contiene el método paso a paso. Cargar solo cuando el WORKER
esté activo según la sección 9.1 del `SKILL.md`.

**Objetivo**:
Detectar inconsistencias sintácticas, semánticas, contractuales,
operacionales y de seguridad.

[SEQUENTIAL_BLOCK]

1. Validar bloques y cierres.
2. Validar nombres canónicos.
3. Validar variables declaradas.
4. Validar tipos.
5. Validar INPUTS y OUTPUTS.
6. Validar WORKERS invocados.
7. Validar rutas.
8. Validar referencias.
9. Validar contratos.
10. Validar estados y ENUM.
11. Validar fórmulas y pesos.
12. Validar intervalos.
13. Validar precedencia de decisiones.
14. Detectar sobrescritura de resultados.
15. Detectar contaminación entre registros.
16. Detectar instrucciones en datos no confiables.
17. Detectar outputs sin validación.
18. Detectar decisiones sin fuente.
19. Clasificar severidad.
20. Registrar ubicación, efecto y corrección recomendada.

[END_SEQUENTIAL_BLOCK]
