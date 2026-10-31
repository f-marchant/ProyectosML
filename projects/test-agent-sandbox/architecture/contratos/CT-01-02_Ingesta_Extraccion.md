# Contrato de Etapa: CT-01-02 (Ingesta -> Extracción)

[DOCUMENT_ID: CONTRACT_CT_01_02]
[DEFINE_STAGE_CONTRACT: CT-01-02]

## Identificación

PRODUCER:
01_Ingesta

CONSUMER:
02_Extraccion

ARTIFACT:
data/interim/posts_raw_<batch_id>.json

FORMAT:
JSON

VERSION:
1.0.0

## Identificador

PRIMARY_ID:
post_id

UNIQUE:
true

## Campos

[DEFINE_FIELDS:]

- NAME: post_id
  TYPE: string
  REQUIRED: true
  NULLABLE: false
  DESCRIPTION: Identificador canónico único (ej. "reddit_12abcde", "x_18492039402")

- NAME: platform
  TYPE: string (enum: "REDDIT", "X", "FORUM")
  REQUIRED: true
  NULLABLE: false
  DESCRIPTION: Red o comunidad de procedencia

- NAME: source_url
  TYPE: string (URL)
  REQUIRED: true
  NULLABLE: false
  DESCRIPTION: Enlace directo permanente al hilo o publicación

- NAME: author_hash
  TYPE: string
  REQUIRED: true
  NULLABLE: false
  DESCRIPTION: Hash anónimo del autor para métricas de concentración sin exponer PII

- NAME: title
  TYPE: string
  REQUIRED: false
  NULLABLE: true
  DESCRIPTION: Título del hilo (si aplica)

- NAME: raw_content
  TYPE: string
  REQUIRED: true
  NULLABLE: false
  DESCRIPTION: Texto completo original sin procesar

- NAME: timestamp_utc
  TYPE: string (ISO8601)
  REQUIRED: true
  NULLABLE: false
  DESCRIPTION: Fecha y hora exacta de la publicación en UTC

- NAME: engagement_metrics
  TYPE: object (upvotes: int, replies: int, reposts: int)
  REQUIRED: true
  NULLABLE: false
  DESCRIPTION: Métricas públicas de tracción del post

[END_FIELDS]

## Integridad

[DEFINE_VALIDATION:]

- IDENTIFIER_UNIQUE: true (no se toleran duplicados de post_id)
- REQUIRED_FIELDS: post_id, platform, source_url, raw_content, timestamp_utc
- TYPE_VALIDATION: Estricta según esquema Pydantic
- DUPLICATE_POLICY: Descarte silencioso previo en etapa 01

[END_VALIDATION]

## Información Faltante

[DEFINE_MISSING_POLICY:]

- REQUIRED_FIELD_MISSING: Rechazo de registro individual (loguear en `logs/quarantine/`)
- OPTIONAL_FIELD_MISSING: Asignar `null` o valor por defecto sin abortar lote

[END_MISSING_POLICY]

[END_STAGE_CONTRACT]
