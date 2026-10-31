# WORKER 22: Validate_Cross_Component_Consistency

**Versión**: 7.3.0

Contrato (INPUTS y OUTPUTS) definido en `SKILL.md`, sección 10, WORKER 22.
Este archivo contiene el método paso a paso. Cargar solo cuando el WORKER
esté activo según la sección 9.1 del `SKILL.md`.

**Objetivo**:
Validar la consistencia integral del entregable.

[SEQUENTIAL_BLOCK]

1. Validar adecuación a plataforma.
2. Validar instrucciones confiables.
3. Validar uso de knowledge.
4. Validar jerarquía.
5. Validar capas.
6. Validar contratos.
7. Validar variables y tipos.
8. Validar capabilities.
9. Validar representación intermedia.
10. Validar reglas.
11. Validar funciones.
12. Validar skills.
13. Validar autoconsistencia.
14. Validar procedencia.
15. Validar pruebas.
16. Validar revisión humana.
17. Validar mecanismos de seguridad.
18. Validar migración.
19. Validar rollback.
20. Validar gobierno y versionado.
21. Corregir únicamente errores formales autorizados (sintaxis, cierres de
    bloque, nombres canónicos, referencias rotas) y registrar cada corrección
    en correction_log con ubicación, valor anterior, valor nuevo y motivo.
22. Repetir validaciones afectadas.
23. Asignar ComplianceStatus por dimensión.
24. Registrar hallazgo, impacto y acción.
25. Determinar resultado general.
26. Registrar riesgos no resueltos.
27. Prohibir cumplimiento predeterminado.
28. Prohibir ocultar hallazgos.
29. Prohibir modificar reglas de negocio para obtener cumplimiento.
30. Prohibir correcciones que no queden registradas en correction_log.

[END_SEQUENTIAL_BLOCK]
