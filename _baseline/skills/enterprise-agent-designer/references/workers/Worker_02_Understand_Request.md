# WORKER 02: Understand_Request

**Versión**: 7.3.0

Contrato (INPUTS y OUTPUTS) definido en `SKILL.md`, sección 10, WORKER 02.
Este archivo contiene el método paso a paso. Cargar solo cuando el WORKER
esté activo según la sección 9.1 del `SKILL.md`.

**Objetivo**:
Determinar el propósito, alcance, modalidad, restricciones y productos
esperados.

[SEQUENTIAL_BLOCK]

1. Identificar el objetivo explícito.
2. Clasificar la modalidad mediante TaskMode.
3. Identificar la arquitectura que debe conservarse.
4. Identificar productos esperados.
5. Identificar restricciones funcionales.
6. Identificar restricciones técnicas.
7. Identificar requisitos de seguridad.
8. Identificar requisitos de revisión humana.
9. Identificar el nivel de determinismo solicitado.
10. Registrar información ausente.
11. Evaluar si la información ausente bloquea algún componente.
12. No volver a solicitar información disponible.
13. No inferir reglas de negocio.
14. Determinar active_workers según la sección 9.1.
15. Registrar el motivo de cada WORKER marcado NO_APLICA.

[END_SEQUENTIAL_BLOCK]
