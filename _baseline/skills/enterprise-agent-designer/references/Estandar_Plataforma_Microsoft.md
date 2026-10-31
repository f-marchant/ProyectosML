# Estándar de Selección de Plataforma Microsoft

[DOCUMENT_ID: MICROSOFT_AGENT_PLATFORM_STANDARD]

[VERSION: 1.0.0]

[DEFINE_STANDARD: MicrosoftAgentPlatform]

## Propósito

Definir criterios para seleccionar entre:

- Microsoft 365 Copilot Agent Builder;
- Microsoft Copilot Studio;
- custom skills;
- flows;
- connectors;
- API plugins;
- Azure Functions;
- scripts;
- revisión humana.

## Agent Builder

Utilizar preferentemente para:

- agentes declarativos;
- instrucciones;
- knowledge sources;
- escenarios de complejidad baja o moderada;
- prototipos;
- capacidades semánticas que no requieran integraciones externas.

## Copilot Studio

Utilizar cuando se requieran:

- acciones;
- connectors;
- topics;
- agent flows;
- workflows;
- integraciones;
- control de orquestación adicional;
- acciones de negocio.

## Custom skills

Utilizar cuando:

- la función sea modular;
- la función sea reusable;
- requiera instrucciones especializadas;
- necesite recursos específicos;
- se beneficie de carga progresiva de contexto.

La disponibilidad deberá verificarse en el tenant.

## Functions y tools

Utilizar para:

- cálculos;
- normalizaciones;
- comparaciones exactas;
- consultas estructuradas;
- conciliaciones;
- transformaciones reproducibles.

## Selección

[DEFINE_DECISION_RULES:]

IF:
- tarea == semantic
- integración_externa == false
THEN:
- preferir AGENT_INSTRUCTION o CUSTOM_SKILL

IF:
- tarea == deterministic
THEN:
- preferir TOOL, FLOW, FUNCTION o SCRIPT

IF:
- requiere_integracion == true
THEN:
- preferir COPILOT_STUDIO o mecanismo pro-code

IF:
- tarea == high_impact_decision
THEN:
- incorporar HUMAN_REVIEW

[END_DECISION_RULES]

## Instrucciones frente a conocimiento

Las instrucciones críticas del agente deberán mantenerse como
instrucciones confiables.

Los knowledge sources deberán aportar:

- hechos;
- normativa;
- taxonomías;
- políticas;
- datos maestros;
- material de consulta.

[DEFINE_CONSTRAINTS:]

- FORBID: Utilizar knowledge sources para sortear límites de instrucciones.
- FORBID: Depender de texto directivo dentro de documentos de conocimiento
  para ejecutar reglas críticas.
- MUST: Tratar knowledge como información recuperada.
- MUST: Mantener las restricciones críticas en componentes confiables.

[END_CONSTRAINTS]

## Matriz de decisión

### Instrucción

Adecuada para:

- rol;
- restricciones;
- comportamiento;
- routing.

### Knowledge

Adecuado para:

- normativa;
- políticas;
- documentación;
- ejemplos subordinados.

### Skill

Adecuada para:

- procedimientos especializados;
- tareas reutilizables;
- capacidades semánticas.

### Tool

Adecuado para:

- exactitud;
- cálculos;
- validación;
- transformación.

### Human Review

Adecuada para:

- decisiones sensibles;
- contradicciones no resolubles;
- baja confianza;
- excepciones.

## Validación previa

Antes de seleccionar plataforma verificar:

- licencia;
- disponibilidad del feature;
- políticas del tenant;
- Information Barriers;
- conectividad;
- sensibilidad;
- residencia de datos;
- capacidades permitidas.

## Criterio de aceptación

La arquitectura cumple cuando cada capability dispone de una
ImplementationType justificada y compatible con el entorno autorizado.

[END_STANDARD]
