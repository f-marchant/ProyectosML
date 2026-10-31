# Contexto Global: Orquestación de Inteligencia de Fricción

[DOCUMENT_ID: CTX_GLOBAL_SOCIAL_FRICTION]
[VERSION: 1.0.0]

[MAIN_FLOW]

## Objetivo

Orquestar de extremo a extremo la captura, extracción semántica, clusterización determinista y síntesis ejecutiva de quejas y fricciones manifestadas por usuarios en redes sociales y foros.

## Etapas

[DEFINE_STAGE_SEQUENCE:]

01_Ingesta
→ 02_Extraccion
→ 03_Agregacion
→ 04_Reporte

[END_STAGE_SEQUENCE]

## Contratos

[DEFINE_INTERSTAGE_CONTRACTS:]

- CONTRACT_ID: CT-01-02
  PRODUCER: 01_Ingesta
  CONSUMER: 02_Extraccion
  ARTIFACT: posts_raw_<batch_id>.json

- CONTRACT_ID: CT-02-03
  PRODUCER: 02_Extraccion
  CONSUMER: 03_Agregacion
  ARTIFACT: claims_friction_<batch_id>.json

- CONTRACT_ID: CT-03-04
  PRODUCER: 03_Agregacion
  CONSUMER: 04_Reporte
  ARTIFACT: topics_aggregated_<batch_id>.json

[END_INTERSTAGE_CONTRACTS]

## Transiciones y Compuertas

[DEFINE_TRANSITIONS:]

- FROM: 01_Ingesta
  TO: 02_Extraccion
  CONDITION: posts_raw_count > 0 AND validation_status == "VALID"
  REVIEW_GATE: NONE

- FROM: 02_Extraccion
  TO: 03_Agregacion
  CONDITION: claims_friction_status == "VALID"
  REVIEW_GATE: NONE

- FROM: 03_Agregacion
  TO: 04_Reporte
  CONDITION: topics_aggregated_status == "VALID"
  REVIEW_GATE: CRITICAL_SPIKE_GATE (si ratio_critico > 0.25 requiere aprobación humana antes de reporte externo)

[END_TRANSITIONS]

## Control de Progreso

[DEFINE_PROGRESS_CONTROL:]

- execution_id: string (UUIDv4)
- current_stage: string (enum: 01_Ingesta, 02_Extraccion, 03_Agregacion, 04_Reporte, COMPLETED, FAILED)
- progress: integer (0 a 100)
- status: string (enum: PENDING, IN_PROGRESS, WAITING_HUMAN_REVIEW, DONE, ERROR)

[END_PROGRESS_CONTROL]

## Reglas Globales

[DEFINE_CONSTRAINTS:]

- MUST: Mantener aislamiento estricto por lote (`batch_id`).
- MUST: Toda métrica cuantitativa de volumen debe coincidir exactamente con el conteo de `post_id` en el artefacto intermedio.
- FORBID: Proceder a la etapa siguiente si la validación del contrato interetapa falla.

[END_CONSTRAINTS]

## Finalización

[DEFINE_RESULT:]

- CONDITION: current_stage == 04_Reporte AND report_generated == true
- OUTPUT: reports/Friction_Report_<batch_id>.md
- REVIEW: Aprobación final por Product Manager o Lead de Soporte.

[END_RESULT]

[END_MAIN_FLOW]
