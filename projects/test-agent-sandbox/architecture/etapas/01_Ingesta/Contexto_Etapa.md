# Contexto de Etapa: 01_Ingesta

[DOCUMENT_ID: CTX_STAGE_01_INGESTA]
[VERSION: 1.0.0]

[MAIN_FLOW]

## Objetivo

Conectar a las APIs públicas de Reddit, X y foros para recopilar publicaciones y comentarios dentro de la ventana de tiempo configurada, deduplicar por hash y emitir el artefacto normalizado de posts.

## Contexto necesario

[DEFINE_CONTEXT_REQUIREMENTS:]

- L0: Identidad y políticas de rate limit de APIs sociales.
- L1: Lista de palabras clave, subreddits y cuentas autorizadas.
- L2: Histórico de identificadores de posts ya procesados (deduplicación).
- L3: Esquema de salida para `posts_raw_<batch_id>.json`.
- L4: Tokens y claves de acceso gestionados por entorno (seguridad).

[END_CONTEXT_REQUIREMENTS]

## Entrada

[DEFINE_INPUT:]

- ARTIFACT: config/sources_and_filters.yaml
- CONTRACT: NONE (Etapa de origen / ingestión)
- REQUIRED: true

[END_INPUT]

## Variables

[DEFINE_VARIABLES:]

- batch_id: string
- time_window_hours: integer
- total_retrieved: integer
- deduplicated_count: integer

[END_VARIABLES]

## Restricciones

[DEFINE_CONSTRAINTS:]

- MUST: Ejecución 100% determinista mediante script (`TOOL-INGEST-001`).
- MUST: Hashear cada publicación (`sha256(platform + post_id)`) para evitar duplicados.
- FORBID: Ingestar datos privados o mensajes directos.

[END_CONSTRAINTS]

## Workflow

[DEFINE_WORKFLOW: StageWorkflow]

EXECUTE IN ORDER:

1. CALL TOOL: TOOL-INGEST-001 (Fetch social posts from configured feeds)
2. CALL SCRIPT: Deduplicate against processed cache
3. CALL SCRIPT: Validate schema CT-01-02

[END_WORKFLOW]

## Output

[DEFINE_OUTPUT:]

- ARTIFACT: data/interim/posts_raw_<batch_id>.json
- CONTRACT: CT-01-02
- VALIDATION: All records have valid id, platform, timestamp, author, and content

[END_OUTPUT]

[END_MAIN_FLOW]
