# DATA_DICTIONARY.md — Diccionario de Datos del MVP

Este documento define el esquema de los datos que consume la aplicación para visualización.

---

## 1. Esquema del Dataset Principal

| Columna | Tipo | Descripción | Rango / Valores esperados |
| :--- | :--- | :--- | :--- |
| `id` | `str / int` | Identificador único del registro | No nulo, único |
| `date` | `date` | Fecha del evento o registro | Formato ISO `YYYY-MM-DD` |
| `category` | `str` | Segmento o categoría de análisis | Categorías conocidas |
| `metric_primary` | `float` | Métrica numérica principal (ej. ventas, predicción, score) | $\ge 0$ |
| `metric_secondary`| `float` | Métrica complementaria (ej. costo, probabilidad, latencia) | Rango variable |
| `status` | `str` | Estado o etiqueta (`OK`, `Warning`, `Critical`) | Valores discretos |

---

## 2. Reglas de Validación
- Todo valor nulo o fuera de rango debe ser imputado o filtrado con advertencia visible en la UI.
- Las fechas deben ser parseadas en timezone consistente (`UTC`).
