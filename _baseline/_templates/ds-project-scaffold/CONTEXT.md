# CONTEXT.md — Pipeline y Contratos de Etapa: {{PROJECT_NAME}}

Este archivo define el flujo de trabajo secuencial del proyecto y los contratos de cada etapa.

---

## 1. Mapa de Contexto (Dónde encontrar qué)

| Carpeta / Archivo | Tipo de Información | Cuándo consultarlo |
| :--- | :--- | :--- |
| `research/` | Sustento teórico, papers, formulación matemática | Al diseñar o justificar algoritmos y métricas |
| `_context/domain.md` | Diccionario de variables y problema de negocio | Al manipular datos y seleccionar variables |
| `_context/conventions.md` | Protocolo de validación estadística y seeds | Al configurar splits y métricas de evaluación |
| `data/` | Datasets por capas (`raw/`, `interim/`, `processed/`) | Para ejecutar scripts de carga y features |
| `notebooks/` | Exploración narrativa y visual | Para experimentos interactivos |
| `src/` | Código modular reutilizable | Para pipelines estables y funciones |
| `reports/` | Figuras, hallazgos y resumen ejecutivo | Al comunicar resultados y conclusiones |

---

## 2. Contratos de Etapa (Pipe & Filter)

### Etapa 01: Formulación y Fundamento Teórico (`research/`)
- **Entrada**: Objetivo del negocio y literatura relevante.
- **Proceso**: Redactar hipótesis, formulación matemática y criterios de evaluación.
- **Salida**: `research/01_problem_formulation.md` y `research/03_methodological_rationale.md`.
- **Superficie de Edición**: Revisar y aprobar los supuestos antes de procesar datos.

### Etapa 02: Análisis Exploratorio de Datos (EDA)
- **Entrada**: `data/raw/` y `_context/domain.md`.
- **Proceso**: Inspeccionar distribuciones, correlaciones, valores nulos y cardinalidad en `notebooks/01_eda/`.
- **Salida**: Gráficos en `reports/figures/` y hallazgos en `reports/summary.md`.

### Etapa 03: Preprocesamiento e Ingeniería de Variables
- **Entrada**: `data/raw/` y hallazgos del EDA.
- **Proceso**: Limpieza, imputación, escalado y creación de variables en `src/data/` y `src/features/`.
- **Salida**: Datasets limpios con split en `data/processed/` (`train.parquet`, `test.parquet`).

### Etapa 04: Modelado y Optimización
- **Entrada**: `data/processed/train.parquet` y protocolo en `_context/conventions.md`.
- **Proceso**: Entrenamiento con validación cruzada y búsqueda de hiperparámetros en `src/models/`.
- **Salida**: Modelos serializados en `models/` y tabla de experimentos.

### Etapa 05: Evaluación e Interpretabilidad
- **Entrada**: `models/` y `data/processed/test.parquet`.
- **Proceso**: Evaluación en test set y cálculo de SHAP values / feature importance.
- **Salida**: Reporte final consolidado en `reports/summary.md`.
