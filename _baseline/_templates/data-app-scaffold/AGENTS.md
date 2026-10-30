# AGENTS.md — {{PROJECT_NAME}} (Aplicación de Datos / Dashboard MVP)

> **Tipo de Proyecto**: Data App / Dashboard Interactivo / Visualización para Usuario Final
> **Objetivo**: {{PROJECT_DESCRIPTION}}
> **Fecha de Creación**: {{CREATION_DATE}}

---

## 1. Dónde estoy y Qué rige
Estás en el proyecto de aplicación de datos `{{PROJECT_NAME}}`. Sigue la metodología ICM:
- **Línea base global**: Respeta `~/.gemini/config/GEMINI.md`.
- **Contrato de Producto**: Consulta `_context/product.md` para entender el problema, la audiencia y las 3 preguntas clave del negocio.
- **Contrato de Diseño**: Consulta `_context/design.md` para tokens de color, tipografía deliberada y restricciones anti "AI Slop".
- **Diccionario de Datos**: Consulta `_context/data_dictionary.md` para esquemas y reglas de datos.

---

## 2. Restricciones Técnicas e Inviolables de UI/UX
1. **Cero "AI Slop"**: Prohibido usar paletas cliché de IA (gradientes púrpura-azul, bordes excesivos, tarjetas dentro de tarjetas). Respeta estrictamente `_context/design.md`.
2. **Desacoplamiento Estricto (Lógica vs. UI)**: Las funciones de carga, filtrado y transformación deben residir en `src/data_loader.py` o submódulos, nunca mezcladas en línea dentro del render de Streamlit.
3. **Caché Obligatorio**: Toda carga de datos o computación pesada debe estar decorada con `@st.cache_data` o `@st.cache_resource`.
4. **Respeto a la Inmutabilidad**: Los datos crudos en `data/raw/` son de solo lectura; la app consume réplicas en `data/sample/` o vistas preparadas.
5. **Calidad y Evals Visuales**: Antes de dar una vista por terminada, revisa con las skills de Impeccable en `.agents/skills/impeccable/`.

---

## 3. Skills de Diseño Impeccable Disponibles (`.agents/skills/impeccable/`)
- `audit`: Realiza un chequeo exhaustivo de accesibilidad, contraste de color y jerarquía de información.
- `critique`: Evalúa la ergonomía UX y el cumplimiento de las metas del usuario final.
- `polish`: Pule detalles de terminación (espaciados, micro-estados, números tabulares).
- `typeset`: Calibra ratios de escala tipográfica y legibilidad.
- `colorize`: Ajusta o restringe la paleta de colores semántica.

---

## 4. Comandos Rápidos
- Ejecutar aplicación localmente: `streamlit run src/app.py`
- Correr tests unitarios: `pytest tests/`
- Linting y formateo de código: `ruff check src/ && ruff format src/`
- Auditar presupuesto de tokens de contexto: `python3 scripts/check_context_budget.py`
- Linter mecánico de diseño (opcional): `npx impeccable detect`
