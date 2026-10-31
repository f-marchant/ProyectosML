# Estándar de Autoconsistencia Selectiva

[DOCUMENT_ID: SELECTIVE_SELF_CONSISTENCY_STANDARD]

[VERSION: 2.0.0]

[DEFINE_STANDARD: SelectiveSelfConsistency]

## Propósito

Regular el uso de varios análisis semánticos independientes para mejorar
la estabilidad de tareas ambiguas.

## Elegibilidad

Una tarea será candidata cuando:

- sea semántica;
- admita diferentes interpretaciones;
- tenga una salida estructurada;
- tenga referencias;
- exista validación posterior.

## Tareas candidatas

- asignación de roles;
- extracción de hechos;
- clasificación candidata;
- similitud semántica;
- selección candidata de criterios.

## Tareas excluidas

- cálculos;
- normalizaciones;
- umbrales;
- conteos;
- escritura mecánica;
- identificación exacta de archivos.

## Variables

[DEFINE_VARIABLES:]

- path_count: number
- consensus_threshold: number
- agreement_score: number
- consensus_status: ConsensusStatus
- disagreement_details: List[text]
- escalation_required: boolean

[END_VARIABLES]

[DEFINE_ENUM: ConsensusStatus]

- CONSENSUS_REACHED
- PARTIAL_AGREEMENT
- NO_CONSENSUS
- NOT_APPLICABLE
- REQUIRES_HUMAN_REVIEW

[END_ENUM]

## Configuración inicial recomendada (sujeta a aprobación)

[DEFINE_DEFAULTS:]

- path_count = 3
- consensus_threshold = 0.6667

[END_DEFAULTS]

Estos valores son una propuesta inicial y no constituyen una regla
normativa. Hasta que el propietario del agente los apruebe:

- se registran como `PROPUESTA_NO_VALIDADA`;
- se declaran en `missing_information` del diseño;
- cualquier valor definido por el propietario prevalece sobre ellos.

Se recomienda calibrarlos con la suite de pruebas del agente antes de
publicar.

## Método

1. Generar análisis independientes.
2. Transformarlos al mismo esquema.
3. Comparar únicamente resultados estructurados.
4. Calcular acuerdo.
5. Si 3/3 coinciden:
   - considerar interpretación estable.
6. Si 2/3 coinciden:
   - seleccionar candidato;
   - reforzar validación.
7. Si menos de 2/3 coinciden:
   - no forzar resultado;
   - escalar.
8. Validar contra fuentes.
9. Validar contra reglas.

## Restricciones

[DEFINE_CONSTRAINTS:]

- MUST: Mantener independencia entre caminos.
- MUST: Registrar discrepancias.
- MUST: Validar posteriormente.
- FORBID: Utilizar consenso como evidencia factual.
- FORBID: Aplicar a funciones deterministas.
- FORBID: Ocultar desacuerdo.
- FORBID: Presentar razonamientos internos como prueba.

[END_CONSTRAINTS]

## Criterio de aceptación

La autoconsistencia es válida cuando:

- aumenta estabilidad sin asumir verdad;
- mantiene procedencia;
- termina en validación simbólica o humana;
- no afecta operaciones deterministas.

[END_STANDARD]
