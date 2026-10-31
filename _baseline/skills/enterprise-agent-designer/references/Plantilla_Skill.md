---
name: skill-name
description: >
  Descripción clara de la capability proporcionada por la skill.
version: 1.0.0
language: es
---

# Skill Name

## Propósito

[Una responsabilidad principal.]

## Activación

Utilizar cuando:

- [Condición.]

No utilizar cuando:

- [Condición.]

## Entradas

- input_name:
  - type:
  - required:
  - source:

## Salidas

- output_name:
  - type:
  - validation:

## Referencias

- `references/...`

## Recursos opcionales

- templates/
- scripts/
- definitions/

## Método

[SEQUENTIAL_BLOCK]

1. Validar inputs.
2. Cargar únicamente referencias necesarias.
3. Ejecutar análisis.
4. Generar salida estructurada.
5. Validar procedencia.
6. Validar restricciones.
7. Devolver resultado.

[END_SEQUENTIAL_BLOCK]

## Restricciones

[DEFINE_CONSTRAINTS:]

- MUST:
- ALLOW:
- FORBID:

[END_CONSTRAINTS]

## Excepciones

- INVALID_INPUT
- MISSING_REFERENCE
- PROCESSING_ERROR
- VALIDATION_ERROR

## Criterios de aceptación

La ejecución es válida cuando:

- los inputs son válidos;
- la salida cumple el esquema;
- existe procedencia;
- no existen inferencias no autorizadas;
- las restricciones se cumplen.
