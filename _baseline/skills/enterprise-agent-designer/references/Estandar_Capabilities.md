# Estándar de Capabilities

[DOCUMENT_ID: ENTERPRISE_AGENT_CAPABILITY_STANDARD]

[VERSION: 1.0.0]

[DEFINE_STANDARD: CapabilityStandard]

## Propósito

Definir cómo identificar, clasificar, implementar y validar capabilities.

## Tipos

[DEFINE_ENUM: CapabilityType]

- SEMANTIC
- SYMBOLIC
- DETERMINISTIC
- GENERATIVE
- ORCHESTRATION
- VALIDATION

[END_ENUM]

## Tipos de implementación

[DEFINE_ENUM: ImplementationType]

- AGENT_INSTRUCTION
- KNOWLEDGE_SOURCE
- CUSTOM_SKILL
- COPILOT_STUDIO_TOPIC
- AGENT_FLOW
- POWER_AUTOMATE_FLOW
- CONNECTOR
- API_PLUGIN
- AZURE_FUNCTION
- SCRIPT
- HUMAN_REVIEW

[END_ENUM]

## Capability mínima

[DEFINE_CAPABILITY_TEMPLATE]

CAPABILITY_ID:

NAME:

PURPOSE:

TYPE:

IMPLEMENTATION:

INPUTS:

OUTPUTS:

REFERENCES:

RULES:

VALIDATION:

ERRORS:

AUTHORITY:

FALLBACK:

VERSION:

OWNER:

[END_CAPABILITY_TEMPLATE]

## SEMANTIC

Utilizar para:

- comprensión;
- extracción;
- similitud;
- desambiguación;
- candidatos.

Debe producir salidas estructuradas.

No deberá producir directamente decisiones críticas cuando exista una
regla posterior.

## SYMBOLIC

Utilizar para:

- aplicar reglas;
- elegibilidad;
- estados;
- taxonomías;
- precedencia.

Debe utilizar RULE_ID.

## DETERMINISTIC

Utilizar para:

- matemáticas;
- normalización;
- fechas;
- identificadores;
- conteos;
- umbrales;
- conciliación.

Debe ser reproducible.

## GENERATIVE

Utilizar para:

- resúmenes;
- narrativas;
- informes;
- preguntas complementarias.

Debe utilizar datos estructurados y resultados ya validados.

## ORCHESTRATION

Utilizar para:

- secuencia;
- routing;
- transiciones;
- retry;
- progreso.

## VALIDATION

Utilizar para:

- contratos;
- fidelidad;
- esquemas;
- documentos;
- reglas;
- seguridad.

## Autoridad

Toda capability deberá definir qué puede y qué no puede modificar.

[DEFINE_CONSTRAINTS:]

- MUST: Definir inputs y outputs.
- MUST: Definir autoridad.
- MUST: Definir mecanismo de validación.
- MUST: Definir fallback cuando sea necesario.
- FORBID: Utilizar capabilities semánticas para cálculos exactos.
- FORBID: Permitir que capabilities generativas cambien decisiones.
- FORBID: Mezclar responsabilidades no relacionadas.

[END_CONSTRAINTS]

## Selección

Si una capability puede implementarse de forma determinista y el
resultado exacto sea importante, deberá preferirse una implementación
determinista.

Si requiere interpretación de lenguaje natural, podrá utilizar una
implementación semántica.

Si combina ambas:

SEMANTIC
→ STRUCTURED OUTPUT
→ SYMBOLIC/DETERMINISTIC

## Criterios de aceptación

Una capability es válida cuando:

- tiene una responsabilidad;
- tiene inputs;
- tiene outputs;
- tiene tipo;
- tiene implementación;
- tiene validación;
- tiene error handling;
- tiene versión;
- no excede su autoridad.

[END_STANDARD]
