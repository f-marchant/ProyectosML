# Registro de Reglas Simbólicas: Clasificación de Severidad de Fricción

[DOCUMENT_ID: RULE_REGISTRY_FRICTION_001]
[VERSION: 1.0.0]

---

[RULE_ID: R-FRIC-001]

NAME:
Criterio_Severidad_Critica

VERSION:
1.0.0

OWNER:
Product Reliability & Operations

STATUS:
ACTIVE

## Propósito
Determinar si un tópico de fricción representa un bloqueo crítico o riesgo inminente de abandono (churn).

## Inputs
- preliminary_category: string
- mentions_count: integer
- sentiment_intensity: float (-1.0 a 0.0)
- contains_data_loss_or_security_keyword: boolean

## Precondition
El tópico debe contener al menos 1 claim validado.

## IF
- contains_data_loss_or_security_keyword == true OR
- (preliminary_category in ["BUG", "BILLING_PRICING"] AND mentions_count >= 15 AND sentiment_intensity <= -0.7)

## THEN
- severity_level = "CRITICAL"
- review_gate_required = true
- escalation_flag = "P0_IMMEDIATE_TRIAGE"

## ELSE
- Evaluar R-FRIC-002

## Priority
1 (Máxima prioridad)

## Tests

### True case
INPUT:
preliminary_category: "BUG", mentions_count: 20, sentiment_intensity: -0.85, contains_data_loss_or_security_keyword: false
EXPECTED:
severity_level == "CRITICAL"

### False case
INPUT:
preliminary_category: "UX_CONFUSION", mentions_count: 5, sentiment_intensity: -0.3, contains_data_loss_or_security_keyword: false
EXPECTED:
severity_level != "CRITICAL"

[END_RULE]

---

[RULE_ID: R-FRIC-002]

NAME:
Criterio_Severidad_Alta

VERSION:
1.0.0

OWNER:
Product Design & Engineering

STATUS:
ACTIVE

## Propósito
Determinar si un tópico de fricción causa degradación funcional severa con workaround complejo.

## Inputs
- preliminary_category: string
- mentions_count: integer
- sentiment_intensity: float

## IF
- (preliminary_category in ["BUG", "PERFORMANCE"] AND mentions_count >= 10) OR
- (preliminary_category in ["UX_CONFUSION", "MISSING_FEATURE"] AND mentions_count >= 25 AND sentiment_intensity <= -0.6)

## THEN
- severity_level = "HIGH"
- review_gate_required = false
- escalation_flag = "P1_BACKLOG_PRIORITY"

## ELSE
- Evaluar R-FRIC-003

## Priority
2

[END_RULE]

---

[RULE_ID: R-FRIC-003]

NAME:
Criterio_Severidad_Media_Baja

VERSION:
1.0.0

STATUS:
ACTIVE

## IF
- mentions_count >= 5

## THEN
- severity_level = "MEDIUM"

## ELSE
- severity_level = "LOW"

## Priority
3

[END_RULE]
