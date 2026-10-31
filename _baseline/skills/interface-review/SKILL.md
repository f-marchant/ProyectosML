---
name: interface-review
description: Audita un git diff, pull request o cambios no confirmados en busca de regresiones o defectos visuales introducidos en la interfaz de usuario (layout, accesibilidad, tipografía, contraste y estados ausentes).
---

# Interface Review — Auditoría de Cambios y Regresiones Visuales

Esta skill revisa un **conjunto de cambios en Git** (diff, commit o PR) en lugar de una pantalla estática, determinando si el cambio introdujo regresiones o descuidó estados esenciales de la interfaz.

## 1. Resolver el Alcance del Cambio (Scope)

Determina el rango de cambios en este orden:
1. Si hay cambios sin confirmar en el árbol de trabajo (`git status -s`), audita los cambios no confirmados.
2. Si la rama actual está adelantada respecto al branch base (`git log @{u}..HEAD`), audita ese rango de commits.
3. Si el usuario indica un commit o PR específico (`HEAD~1..HEAD` o número de PR), audita ese objetivo exacto.

Identifica los archivos modificados que impactan la interfaz (`.py`, `.css`, `.tsx`, `.jsx`, `.html`, `.vue`, etc.), excluyendo lockfiles, artefactos generados o binarios.

---

## 2. Radio de Impacto (Blast Radius)

Un archivo modificado no es solo lo que contiene el diff:
- **Componentes directos**: Revisa los archivos que importan o consumen directamente el componente o módulo modificado.
- **Tokens o estilos globales**: Si se modificó un archivo de estilos (`custom.css`, tokens de color, variables globales), el impacto abarca todas las pantallas que usan dichos tokens.

---

## 3. Inspección del Diff: Lo que se Añadió y lo que se Eliminó

1. **Líneas eliminadas (`-`)**: ¿Se eliminó una etiqueta accesible (`aria-label`, `alt`), un estado de carga, o una clase de responsive design sin sustituto?
2. **Líneas agregadas (`+`)**: ¿Cumplen con los contratos de diseño del proyecto (`_context/design.md`)?

---

## 4. Búsqueda de Estados Olvidados (Incomplete Changes)

Un diff suele descuidar los estados que no estaban en el caso feliz:
- [ ] **Estado Vacío (Empty State)**: ¿Qué ocurre si la consulta devuelve cero registros o una lista vacía? ¿Muestra un mensaje claro o una región en blanco rota?
- [ ] **Estado de Carga (Loading)**: ¿Hay feedback visual mientras se obtienen datos pesados?
- [ ] **Estado de Error / Falla**: ¿Se capturan excepciones con un mensaje útil en lenguaje del usuario?
- [ ] **Desborde (Overflow)**: ¿Qué pasa si el texto es 3 veces más largo de lo previsto? ¿Se trunca o rompe el contenedor?
- [ ] **Accesibilidad (A11y)**: ¿Los elementos interactivos nuevos tienen contraste adecuado y foco navegable por teclado?

---

## 5. Clasificación y Reporte de Hallazgos

Clasifica cada problema detectado bajo una de tres categorías:
- **`Introduced`**: Defecto visual o de accesibilidad creado directamente por el cambio.
- **`Regression`**: El cambio debilitó o rompió algo que antes funcionaba correctamente.
- **`Pre-existing`**: Problema que ya existía antes del cambio y que este diff no empeoró (menciónalo solo como nota al margen).

### Formato del Reporte

```markdown
### 📋 Reporte de Interface Review

**Objetivo evaluado**: [Rama, commit o archivos modificados]
**Superficies impactadas**: [Vistas o componentes afectados]

| Tipo | Archivo / Componente | Hallazgo Observado | Corrección Recomendada |
| :--- | :--- | :--- | :--- |
| `Regression` | `src/components/kpis.py` | Se eliminó el formateo tabular numérico | Restaurar `tabular-nums` |
| `Introduced` | `src/components/charts.py`| Falta manejar caso con 0 registros | Añadir condición de fallback |

**Veredicto**: [Block (requiere corrección antes de merge) | Approve (aprobado)]
```
