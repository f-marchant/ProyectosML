# Estándar de Pruebas para Agentes Empresariales

[DOCUMENT_ID: ENTERPRISE_AGENT_TEST_STANDARD]

[VERSION: 1.0.0]

[DEFINE_STANDARD: EnterpriseAgentTesting]

## Propósito

Establecer pruebas reproducibles para validar agentes antes y después de
cambios.

## Tipos de prueba

[DEFINE_ENUM: TestType]

- CONTRACT_TEST
- RULE_TEST
- FUNCTION_TEST
- BOUNDARY_TEST
- SKILL_TEST
- REGRESSION_TEST
- SECURITY_TEST
- DOCUMENT_TEST
- MODEL_CHANGE_TEST

[END_ENUM]

## Test Case

[DEFINE_TYPE: TestCase]

TestCase = {
  test_id: text,
  test_type: TestType,
  purpose: text,
  inputs: object,
  expected_output: object,
  acceptance_condition: text,
  version: text
}

[END_TYPE]

## Contract tests

Verificar:

- campos;
- tipos;
- identificadores;
- obligatoriedad;
- compatibilidad productor-consumidor.

## Rule tests

Por cada RULE_ID incluir:

- condición verdadera;
- condición falsa;
- límites;
- conflicto;
- precedencia.

## Function tests

Verificar:

- mismo input produce mismo output;
- errores;
- valores nulos;
- formatos inválidos.

## Boundary tests

Obligatorios para:

- umbrales;
- escalas;
- rangos;
- fechas límite;
- porcentajes.

Probar:

- inmediatamente inferior;
- exactamente igual;
- inmediatamente superior.

## Skill tests

Verificar:

- activación;
- inputs;
- output schema;
- referencias;
- restricciones;
- errores.

## Regression tests

Crear baseline aprobado.

Comparar cambios en:

- clasificación;
- cálculos;
- decisiones;
- narrativa;
- archivos;
- estados.

## Security tests

Incluir:

- instrucciones dentro de datos;
- enlaces;
- comandos;
- contenido contradictorio;
- datos de otro caso;
- intento de acceso no autorizado.

## Model change tests

Ante cambios relevantes de modelo o comportamiento:

- ejecutar baseline;
- comparar métricas;
- identificar regresiones;
- revalidar tasks semánticas.

## Métricas mínimas

- contract_pass_rate
- rule_pass_rate
- function_pass_rate
- provenance_coverage
- output_schema_compliance
- human_correction_rate
- regression_difference_rate

## Reglas

[DEFINE_CONSTRAINTS:]

- MUST: Toda función determinista tendrá tests.
- MUST: Toda regla crítica tendrá tests.
- MUST: Los gates utilizarán tests.
- MUST: Usar datos sintéticos o autorizados.
- FORBID: Usar production data innecesariamente.
- FORBID: Aprobar una versión con fallos críticos.
- FORBID: Cambiar el expected result para ocultar una regresión.

[END_CONSTRAINTS]

## Criterios sugeridos de aceptación

Para componentes deterministas críticos:

- function_pass_rate = 100 %
- contract_pass_rate = 100 %
- rule_pass_rate = 100 %

Para procedencia:

- provenance_coverage = 100 % en afirmaciones sustantivas.

Las métricas semánticas deberán establecerse según el dominio y revisión
humana.

[END_STANDARD]
