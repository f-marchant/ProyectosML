# Plantilla de Contrato de Tool o Función

[DOCUMENT_ID: TOOL_CONTRACT_TEMPLATE]

[DEFINE_TOOL_CONTRACT: ToolName]

## Propósito

[Operación determinista.]

## Implementation

TYPE:
[AGENT_FLOW | POWER_AUTOMATE_FLOW | CONNECTOR | API_PLUGIN |
AZURE_FUNCTION | SCRIPT]

VERSION:
[Versión.]

## Inputs

[DEFINE_INPUTS:]

- NAME:
  TYPE:
  REQUIRED:
  VALIDATION:

[END_INPUTS]

## Outputs

[DEFINE_OUTPUTS:]

- NAME:
  TYPE:
  DESCRIPTION:

[END_OUTPUTS]

## Errors

[DEFINE_ERRORS:]

- CODE:
  MEANING:
  RETRYABLE:

[END_ERRORS]

## Determinismo

[DEFINE_DETERMINISM:]

SAME_INPUT_SAME_OUTPUT:
true

SIDE_EFFECTS:
[none | documented]

ROUNDING:
[Regla.]

PRECISION:
[Regla.]

[END_DETERMINISM]

## Validación

[DEFINE_VALIDATION:]

- Input schema.
- Output schema.
- Boundary conditions.
- Error conditions.

[END_VALIDATION]

## Tests

- TEST_ID:
- INPUT:
- EXPECTED_OUTPUT:

## Restricciones

[DEFINE_CONSTRAINTS:]

- MUST: Validar tipos.
- MUST: Registrar versión.
- MUST: Tener pruebas.
- FORBID: Inferir valores faltantes.
- FORBID: Modificar parámetros durante ejecución.

[END_CONSTRAINTS]

[END_TOOL_CONTRACT]
