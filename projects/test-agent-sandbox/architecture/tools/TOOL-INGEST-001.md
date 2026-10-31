# Contrato de Tool: TOOL-INGEST-001 (Social Feed Fetcher & Normalizer)

[DOCUMENT_ID: TOOL_CONTRACT_INGEST_001]
[DEFINE_TOOL_CONTRACT: TOOL-INGEST-001]

## Propósito
Ingestar publicaciones y comentarios desde Reddit API, X API v2 y foros configurados, normalizando fechas a UTC y descartando duplicados mediante cálculo de hash determinista.

## Implementation
TYPE: SCRIPT (Python 3.11 / Connector)
VERSION: 1.0.0

## Inputs

[DEFINE_INPUTS:]

- NAME: config_path
  TYPE: string (File path)
  REQUIRED: true
  VALIDATION: Debe existir archivo YAML con credenciales y fuentes.

- NAME: window_hours
  TYPE: integer
  REQUIRED: true
  VALIDATION: window_hours > 0 AND window_hours <= 168 (máximo 7 días).

[END_INPUTS]

## Outputs

[DEFINE_OUTPUTS:]

- NAME: output_file_path
  TYPE: string
  DESCRIPTION: Ruta absoluta al archivo `posts_raw_<batch_id>.json` generado.

- NAME: total_retrieved
  TYPE: integer
  DESCRIPTION: Conteo bruto de publicaciones recuperadas.

- NAME: deduplicated_count
  TYPE: integer
  DESCRIPTION: Conteo neto tras eliminar hashes previamente procesados.

[END_OUTPUTS]

## Errores y Excepciones

[DEFINE_ERRORS:]

- CODE: ERR_RATE_LIMIT
  MEANING: API de la plataforma devolvió HTTP 429 Too Many Requests.
  RETRYABLE: true (esperar backoff exponencial hasta 3 intentos).

- CODE: ERR_AUTH_FAILURE
  MEANING: Token o API Key caducada o sin permisos de lectura.
  RETRYABLE: false (abortar y emitir alerta administrativa).

[END_ERRORS]

## Determinismo

[DEFINE_DETERMINISM:]

SAME_INPUT_SAME_OUTPUT: true (para un snapshot temporal fijo)
SIDE_EFFECTS: none (operación de lectura pura)
ROUNDING: N/A
PRECISION: N/A

[END_DETERMINISM]

[END_TOOL_CONTRACT]
