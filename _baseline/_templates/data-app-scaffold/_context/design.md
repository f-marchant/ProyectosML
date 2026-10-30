# DESIGN.md — Contrato de Sistema Visual y Directrices UI (Impeccable)

Este documento define el lenguaje visual y las restricciones de interfaz para evitar el "AI Slop" y garantizar un diseño sobrio, profesional y usable.

---

## 1. Tokens de Color

Paleta deliberada, de alto contraste y restringida:
- **Fondo Principal**: `#0F172A` (Slate 900 - Oscuro sobrio) o `#F8FAFC` (Slate 50 en modo claro).
- **Superficie de Tarjetas / Paneles**: `#1E293B` (Slate 800) con bordes sutiles `#334155`.
- **Acento Primario**: `#38BDF8` (Sky 400 - claridad y foco visual).
- **Acento de Estado Positivo**: `#34D399` (Emerald 400).
- **Acento de Alerta / Negativo**: `#F87171` (Red 400).
- **Texto Principal**: `#F1F5F9` (Slate 100 - legible sin deslumbramiento).
- **Texto Secundario / Metadatos**: `#94A3B8` (Slate 400).

---

## 2. Tipografía y Jerarquía
- **Familia Primaria**: Sistema nativo sans-serif (`-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif`). Evitar cargar fuentes genéricas pesadas en línea si ralentizan el render.
- **Jerarquía**:
  * Título de vista: 24px–28px, peso 600, espaciado equilibrado.
  * KPI Valor: 32px–36px, tabular numbers (`font-variant-numeric: tabular-nums`).
  * Cuerpo de texto: 14px–15px, interlineado 1.5.
  * Etiquetas / Captions: 12px, tono apagado (`#94A3B8`).

---

## 3. Anti-Patrones Prohibidos (Anti "AI Slop")
1. ❌ **No gradientes púrpura-azul cliché**: Usar fondos sólidos planos con suficiente separación tonal.
2. ❌ **No cards anidadas dentro de cards**: Mantener una superficie visual plana con divisores limpios.
3. ❌ **No textos en ALL CAPS con espaciado excesivo** en cada subtítulo o tarjeta.
4. ❌ **No bordes redondeados excesivos (`rounded-3xl` o píldoras)** para contenedores de datos tabulares.
5. ❌ **No saturación de gráficos**: Un gráfico por sección lógica; no meter 6 gráficos tipo donut o pie charts sin valor informativo.

---

## 4. Estilo de Gráficos (Plotly / Visualización)
- Fondos de gráfico transparentes (`paper_bgcolor='rgba(0,0,0,0)'`, `plot_bgcolor='rgba(0,0,0,0)'`).
- Gridlines tenues en color neutro (`rgba(148, 163, 184, 0.15)`).
- Etiquetas de ejes legibles en `#94A3B8` con tamaño 12px.
- Tooltips limpios y formateados con unidades exactas (ej. `$`, `%`, `N`).
