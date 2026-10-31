# Contexto de Etapa: 03_Agregacion

[DOCUMENT_ID: CTX_STAGE_03_AGREGACION]
[VERSION: 1.0.0]

[MAIN_FLOW]

## Objetivo

Agrupar los claims individuales de fricción en tópicos o temas consolidados mediante clustering semántico guiado por reglas simbólicas, calcular el volumen e impacto cuantitativo determinista y evaluar si se disparan alertas de severidad crítica.

## Contexto necesario

[DEFINE_CONTEXT_REQUIREMENTS:]

- L0: Catálogo canónico de tópicos conocidos y umbrales de alerta (`Rule_Registry.md`).
- L1: Algoritmo determinista de clusterización y conteo.
- L2: Histórico de frecuencia de tópicos para cálculo de desviaciones (spikes).
- L3: Esquema de salida de tópicos agregados (`topics_aggregated_<batch_id>.json`).
- L4: Lista de claims de la etapa 02.

[END_CONTEXT_REQUIREMENTS]

## Entrada

[DEFINE_INPUT:]

- ARTIFACT: data/interim/claims_friction_<batch_id>.json
- CONTRACT: CT-02-03
- REQUIRED: true

[END_INPUT]

## Variables

[DEFINE_VARIABLES:]

- total_claims_evaluated: integer
- distinct_topics_count: integer
- top_critical_topic_id: string
- critical_spike_detected: boolean

[END_VARIABLES]

## Restricciones

[DEFINE_CONSTRAINTS:]

- MUST: Conteo de menciones y métricas de engagement 100% deterministas (`TOOL-CLUSTER-001`).
- MUST: Aplicar reglas de severidad `R-FRIC-001` a `R-FRIC-003` sin omitir condiciones.
- ALWAYS: Si `critical_spike_detected == true`, activar bandera de compuerta humana.

[END_CONSTRAINTS]

## Workflow

[DEFINE_WORKFLOW: StageWorkflow]

EXECUTE IN ORDER:

1. CALL TOOL: TOOL-CLUSTER-001 (Deterministic aggregation & mention count)
2. CALL CAPABILITY: CAP-003 (Apply symbolic rules from Rule_Registry.md)
3. CALL SCRIPT: Anomaly_Spike_Detector (evaluar umbrales de alerta)
4. CALL SCRIPT: Validate schema CT-03-04

[END_WORKFLOW]

## Output

[DEFINE_OUTPUT:]

- ARTIFACT: data/interim/topics_aggregated_<batch_id>.json
- CONTRACT: CT-03-04
- VALIDATION: Sum of claims per topic matches total friction claims

[END_OUTPUT]

## Review Gate

[DEFINE_REVIEW_GATE:]

- REQUIRED: conditional (si critical_spike_detected == true)
- CONDITION: ratio_critico > 0.25 OR menciones_criticas_absolutas > 50
- APPROVER: Lead Product Manager / Support Commander
- INVALIDATION_SCOPE: 04_Reporte (el reporte final no puede publicarse hasta recibir visto bueno del incidente)

[END_REVIEW_GATE]

[END_MAIN_FLOW]
