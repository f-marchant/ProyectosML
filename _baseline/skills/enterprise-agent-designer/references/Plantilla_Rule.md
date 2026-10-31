# Plantilla de Regla Simbólica

[DOCUMENT_ID: SYMBOLIC_RULE_TEMPLATE]

[RULE_ID: DOMAIN-000]

NAME:
[Nombre.]

VERSION:
1.0.0

OWNER:
[Propietario.]

STATUS:
ACTIVE

## Propósito

[Qué determina.]

## Inputs

- [Variable.]
- [Tipo.]

## Precondition

[Condiciones necesarias.]

## IF

- [Condición.]

## THEN

- [Resultado.]

## ELSE

- [Resultado alternativo.]

## Source

- [Normativa.]
- [Referencia.]
- [Versión.]

## Priority

[Valor.]

## Conflicts

- [RULE_ID potencialmente conflictiva.]

## Decision trace

Registrar:

- RULE_ID;
- inputs utilizados;
- condición evaluada;
- resultado;
- timestamp;
- versión.

## Tests

### True case

INPUT:
[Valores.]

EXPECTED:
[Resultado.]

### False case

INPUT:
[Valores.]

EXPECTED:
[Resultado.]

### Boundary case

INPUT:
[Valores.]

EXPECTED:
[Resultado.]

## Restricciones

[DEFINE_CONSTRAINTS:]

- MUST: Utilizar únicamente inputs autorizados.
- MUST: Mantener versión.
- MUST: Tener tests.
- FORBID: Cambiar prioridad durante ejecución.
- FORBID: Sustituir condiciones por confianza del modelo.
- FORBID: Utilizar ejemplos como fuente normativa.

[END_CONSTRAINTS]

[END_RULE]
