# Contexto de Etapa: 04_Reporte

[DOCUMENT_ID: CTX_STAGE_04_REPORTE]
[VERSION: 1.0.0]

[MAIN_FLOW]

## Objetivo

Generar un informe ejecutivo estructurado en Markdown que sintetice los principales tópicos de fricción, clasificados por severidad, con estadísticas verificadas, ejemplos textuales citados y recomendaciones accionables para los equipos de producto e ingeniería.

## Contexto necesario

[DEFINE_CONTEXT_REQUIREMENTS:]

- L0: Plantilla ejecutiva de informe de fricción (`reports/templates/executive_summary_template.md`).
- L1: Pautas de redacción (concisión, objetividad, orientación a acción).
- L2: Dataset agregado de tópicos con conteos deterministas.
- L3: Esquema de reporte final en Markdown.
- L4: Estado de la compuerta de revisión humana.

[END_CONTEXT_REQUIREMENTS]

## Entrada

[DEFINE_INPUT:]

- ARTIFACT: data/interim/topics_aggregated_<batch_id>.json
- CONTRACT: CT-03-04
- REQUIRED: true

[END_INPUT]

## Variables

[DEFINE_VARIABLES:]

- report_id: string
- total_friction_topics: integer
- high_priority_topics_count: integer
- output_report_path: string

[END_VARIABLES]

## Restricciones

[DEFINE_CONSTRAINTS:]

- MUST: Todo número o porcentaje en el texto narrativo debe coincidir con el JSON de entrada.
- MUST: Toda recomendación debe estar vinculada a un `topic_id` existente.
- FORBID: Inventar citas testimoniales que no figuren en los claims del lote.
- FORBID: Publicar automáticamente si `critical_spike_detected` no fue aprobado por humanos.

[END_CONSTRAINTS]

## Workflow

[DEFINE_WORKFLOW: StageWorkflow]

EXECUTE IN ORDER:

1. CALL CAPABILITY: CAP-004 (Generative Executive Synthesis)
2. CALL CAPABILITY: CAP-005 (Cross-validation & claim fidelity check)
3. CALL SCRIPT: Markdown_Linter (verificar formato y enlaces)
4. EMIT: reports/Friction_Intelligence_Report_<batch_id>.md

[END_WORKFLOW]

## Output

[DEFINE_OUTPUT:]

- ARTIFACT: reports/Friction_Intelligence_Report_<batch_id>.md
- CONTRACT: NONE (Artefacto final de entrega para stakeholders)
- VALIDATION: 100% of claims cited have valid traceable URLs to original posts

[END_OUTPUT]

[END_MAIN_FLOW]
