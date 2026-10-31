# Esquema de Representación Intermedia

[DOCUMENT_ID: INTERMEDIATE_REPRESENTATION_STANDARD]

[VERSION: 2.0.0]

## Propósito

Estabilizar el significado extraído desde contenido no estructurado antes
de activar reglas o cálculos.

[DEFINE_ENUM: InformationType]

- OBJECTIVE_DATA
- REPORTED_FACT
- PERCEPTION
- ANALYSIS_RESULT
- MISSING_INFORMATION
- CONTRADICTION
- CANDIDATE_RULE

[END_ENUM]

[DEFINE_ENUM: ValidationStatus]

- PENDING
- VALID
- INVALID
- REQUIRES_REVIEW
- NOT_APPLICABLE

[END_ENUM]

[DEFINE_TYPE: Claim]

Claim = {
  claim_id: text,
  value: text,
  information_type: InformationType,
  source_id: text,
  source_field: text,
  source_location: text,
  rule_id: text,
  transformation: text,
  attribution_required: boolean,
  confidence: number,
  validation_status: ValidationStatus
}

[END_TYPE]

[DEFINE_TYPE: Contradiction]

Contradiction = {
  contradiction_id: text,
  claim_a: claim_id,
  claim_b: claim_id,
  description: text,
  resolution_status: ValidationStatus
}

[END_TYPE]

[DEFINE_TYPE: CaseRepresentation]

CaseRepresentation = {
  case_id: text,
  execution_id: text,
  objective_data: List[Claim],
  identities: List[Claim],
  participants: List[Claim],
  roles: List[Claim],
  reported_facts: List[Claim],
  perceptions: List[Claim],
  classifications: List[Claim],
  dates: List[Claim],
  periods: List[Claim],
  locations: List[Claim],
  consequences: List[Claim],
  contradictions: List[Contradiction],
  missing_information: List[Claim],
  candidate_rules: List[Claim],
  source_trace: List[Claim],
  validation_status: ValidationStatus
}

[END_TYPE]

## Formación de claims

Cada afirmación sustantiva extraída deberá convertirse en un Claim.

Un claim deberá conservar:

- contenido;
- categoría;
- fuente;
- ubicación;
- atribución;
- validación.

## Datos objetivos

Ejemplos:

- identificador;
- fecha registrada;
- estado administrativo;
- valor almacenado.

## Hechos reportados

Corresponden a acciones o circunstancias relatadas.

No equivalen a hechos acreditados.

## Percepciones

Corresponden a:

- opiniones;
- valoraciones;
- interpretaciones;
- calificaciones.

## Contradicciones

Cuando dos claims sean incompatibles:

- conservar ambos;
- crear Contradiction;
- no seleccionar automáticamente uno;
- escalar si afecta una decisión crítica.

## Información faltante

La información no disponible deberá representarse explícitamente.

No deberá interpretarse como inexistencia.

## Procedencia

Todo claim deberá permitir reconstruir:

source
→ extraction
→ transformation
→ validation
→ use

[DEFINE_CONSTRAINTS:]

- MUST: Todo claim sustantivo tendrá fuente.
- MUST: Mantener atribución.
- MUST: Mantener contradicciones.
- MUST: Registrar transformación.
- ALLOW: Confidence para interpretación semántica.
- FORBID: Confidence como sustituto de regla.
- FORBID: Inventar valores.
- FORBID: Resolver contradicciones mediante probabilidad.
- FORBID: Eliminar claims originales durante una transformación.

[END_CONSTRAINTS]

## Criterio de aceptación

Una representación es válida cuando:

- todos los claims tienen fuente;
- las categorías son coherentes;
- las contradicciones permanecen visibles;
- la ausencia está representada;
- pueden aplicarse reglas posteriores sin volver a interpretar
  necesariamente el texto completo.
