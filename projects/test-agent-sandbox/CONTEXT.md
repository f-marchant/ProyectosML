# CONTEXT.md — Arquitectura Agéntica y Contratos: test-agent-sandbox

Este archivo define el flujo de razonamiento y los componentes del sistema agéntico.

---

## 1. Mapa de Contexto

| Carpeta / Archivo | Tipo de Información | Cuándo consultarlo |
| :--- | :--- | :--- |
| `architecture/Agente.md` | Definición del Agente Raíz, persona, autoridad y restricciones | Al auditar el alcance global y límites |
| `architecture/contexto/` | Contexto Global y secuencia de etapas (L0 a L4) | Al orquestar la ejecución macro |
| `architecture/etapas/` | Contextos específicos por etapa (01_Ingesta a 04_Reporte) | Al ejecutar o modificar una fase |
| `architecture/contratos/` | Esquemas de datos interetapa (CT-01-02, CT-02-03, CT-03-04) | Al validar contratos de datos y JSON |
| `architecture/reglas/` | Registro de reglas simbólicas formales (R-FRIC-001 a 003) | Al modificar criterios de severidad |
| `architecture/tools/` | Contratos de herramientas deterministas (TOOL-INGEST-001) | Al implementar conectores de datos |
| `architecture/pruebas/` | Suite de pruebas (contrato, seguridad, reglas, procedencia) | Al validar calidad y no regresión |
| `_context/persona.md` | Personalidad, rol, tono y límites del agente | Al ajustar comportamiento de chat |
| `_context/safety_guardrails.md` | Políticas de seguridad y aislamiento de contenido | Al validar mitigaciones de injection |
| `src/` | Bucle de ejecución (Python / LangGraph / ReAct) | Al orquestar el flujo de decisiones |

---

## 2. Flujo de Ejecución Agéntica (Enterprise Standard)
1. **01_Ingesta (Determinista)**: Ingesta publicaciones de Reddit, X y Foros vía `TOOL-INGEST-001` y valida contrato `CT-01-02`.
2. **02_Extracción (Semántica)**: Extrae citas textuales (`verbatim_quote`) enmarcadas en `<untrusted_user_text>` y valida contrato `CT-02-03`.
3. **03_Agregación (Simbólica & Determinista)**: Conteo determinista y clasificación de severidad vía `Rule_Registry.md`. Si hay spike crítico, dispara compuerta de revisión humana.
4. **04_Reporte (Generativa & Validación)**: Síntesis ejecutiva con 100% de procedencia verificada hacia las URLs de origen.
