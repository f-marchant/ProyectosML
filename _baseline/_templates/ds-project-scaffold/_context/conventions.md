# Convenciones Técnicas y Estadísticas: {{PROJECT_NAME}}

## 1. Protocolo de Validación Estadística
- **Estrategia de Split**:
  - Datos tabulares independientes: `StratifiedKFold(n_splits=5, shuffle=True, random_state=42)`
  - Series temporales: `TimeSeriesSplit` o validación basada en fecha fija (respetando causalidad temporal).
- **Semilla Global**: `SEED = 42` (utilizada en numpy, torch, sklearn, etc.).
- **Métricas Primarias**:
  - Clasificación desbalanceada: PR-AUC, F1-Score (macro), ROC-AUC.
  - Regresión: RMSE, MAE, $R^2$.

---

## 2. Convenciones de Código
- Tipado estricto con `type hints` en funciones y clases de `src/`.
- Docstrings concisos explicando entradas, salidas y supuestos.
- Formateo automático con `ruff`.
