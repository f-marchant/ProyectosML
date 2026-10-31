# Contrato de Etapa: CT-02-03 (Extracción -> Agregación)

[DOCUMENT_ID: CONTRACT_CT_02_03]
[DEFINE_STAGE_CONTRACT: CT-02-03]

## Identificación

PRODUCER:
02_Extraccion

CONSUMER:
03_Agregacion

ARTIFACT:
data/interim/claims_friction_<batch_id>.json

FORMAT:
JSON

VERSION:
1.0.0

## Identificador

PRIMARY_ID:
claim_id

UNIQUE:
true

## Campos

[DEFINE_FIELDS:]

- NAME: claim_id
  TYPE: string (UUIDv4)
  REQUIRED: true
  NULLABLE: false
  DESCRIPTION: Identificador único del claim de fricción detectado

- NAME: source_post_id
  TYPE: string
  REQUIRED: true
  NULLABLE: false
  DESCRIPTION: Referencia foránea al post_id de origen

- NAME: platform
  TYPE: string
  REQUIRED: true
  NULLABLE: false
  DESCRIPTION: Plataforma social de origen

- NAME: source_url
  TYPE: string (URL)
  REQUIRED: true
  NULLABLE: false
  DESCRIPTION: Enlace para trazabilidad y auditoría humana

- NAME: verbatim_quote
  TYPE: string
  REQUIRED: true
  NULLABLE: false
  DESCRIPTION: Cita textual exacta extraída del post que respalda el reclamo

- NAME: normalized_problem_statement
  TYPE: string
  REQUIRED: true
  NULLABLE: false
  DESCRIPTION: Enunciado conciso y neutral del problema extraído

- NAME: preliminary_category
  TYPE: string (enum: "BUG", "PERFORMANCE", "UX_CONFUSION", "MISSING_FEATURE", "BILLING_PRICING", "CUSTOMER_SUPPORT")
  REQUIRED: true
  NULLABLE: false
  DESCRIPTION: Categoría funcional preliminar

- NAME: sentiment_intensity
  TYPE: float (rango -1.0 a 0.0)
  REQUIRED: true
  NULLABLE: false
  DESCRIPTION: Magnitud de negatividad o frustración detectada

- NAME: engagement_weight
  TYPE: integer
  REQUIRED: true
  NULLABLE: false
  DESCRIPTION: Peso ponderado según upvotes y réplicas del post origen

[END_FIELDS]

## Integridad

[DEFINE_VALIDATION:]

- IDENTIFIER_UNIQUE: true
- FIDELITY_CHECK: verbatim_quote debe ser obligatoriamente subcadena del post original
- REQUIRED_FIELDS: claim_id, source_post_id, verbatim_quote, preliminary_category

[END_VALIDATION]

[END_STAGE_CONTRACT]
