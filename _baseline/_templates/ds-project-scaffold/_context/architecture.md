# Contexto de Arquitectura y Datos: {{PROJECT_NAME}}

## 1. Flujo de Datos (Data Pipeline)
1. **Extracción / Carga**: Fuentes de datos crudos hacia `data/raw/`.
2. **Procesamiento**: Transformaciones reproducibles en `src/data/` emitiendo a `data/interim/` y `data/processed/`.
3. **Formato de Almacenamiento**:
   - Preferir `.parquet` para datos tabulares (eficiencia de I/O, compresión y conservación de tipos).

---

## 2. Entorno de Ejecución y Dependencias
- **Python**: >= 3.10
- **Librerías Principales**: Polars / Pandas, Scikit-learn, LightGBM / XGBoost, PyTorch (si aplica).
- **Aceleración**: CPU / GPU según disponibilidad.
