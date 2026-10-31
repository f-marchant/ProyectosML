# Contrato de Etapa: CT-03-04 (Agregación -> Reporte)

[DOCUMENT_ID: CONTRACT_CT_03_04]
[DEFINE_STAGE_CONTRACT: CT-03-04]

## Identificación

PRODUCER:
03_Agregacion

CONSUMER:
04_Reporte

ARTIFACT:
data/interim/topics_aggregated_<batch_id>.json

FORMAT:
JSON

VERSION:
1.0.0

## Identificador

PRIMARY_ID:
topic_id

UNIQUE:
true

## Campos

[DEFINE_FIELDS:]

- NAME: topic_id
  TYPE: string (ej. "TOPIC_LOGIN_OAUTH_TIMEOUT")
  REQUIRED: true
  NULLABLE: false
  DESCRIPTION: Identificador canónico del tópico o clúster de problema

- NAME: topic_title
  TYPE: string
  REQUIRED: true
  NULLABLE: false
  DESCRIPTION: Título descriptivo del dolor del usuario

- NAME: severity_level
  TYPE: string (enum: "CRITICAL", "HIGH", "MEDIUM", "LOW")
  REQUIRED: true
  NULLABLE: false
  DESCRIPTION: Nivel de severidad asignado deterministamente por reglas simbólicas

- NAME: total_mentions
  TYPE: integer
  REQUIRED: true
  NULLABLE: false
  DESCRIPTION: Conteo exacto de menciones y posts que alimentan este tópico

- NAME: aggregated_engagement
  TYPE: integer
  REQUIRED: true
  NULLABLE: false
  DESCRIPTION: Suma total de upvotes y retweets asociados

- NAME: platforms_involved
  TYPE: array of strings
  REQUIRED: true
  NULLABLE: false
  DESCRIPTION: Canales donde se detectó el problema (Reddit, X, etc.)

- NAME: representative_claims
  TYPE: array of objects (source_url, verbatim_quote, claim_id)
  REQUIRED: true
  NULLABLE: false
  DESCRIPTION: Muestra de citas testimoniales reales para ilustrar el reporte

- NAME: applied_rule_id
  TYPE: string
  REQUIRED: true
  NULLABLE: false
  DESCRIPTION: ID de la regla de Rule_Registry.md que determinó la severidad

[END_FIELDS]

## Integridad

[DEFINE_VALIDATION:]

- IDENTIFIER_UNIQUE: true
- QUANTITATIVE_INTEGRITY: sum(total_mentions) == total_claims_in_batch
- SEVERITY_AUDIT: severity_level debe corresponder exactamente a la lógica de applied_rule_id

[END_VALIDATION]

[END_STAGE_CONTRACT]
