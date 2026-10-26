# 03. Justificación Metodológica de Decisiones de Diseño

> **Proyecto**: {{PROJECT_NAME}}

Este documento registra el *por qué* detrás de cada decisión técnica fundamental (algoritmo, preprocesamiento, métrica).

---

## 1. Justificación de la Familia de Modelos
- **Decisión**: (Ej. Selección de LightGBM / CatBoost frente a Redes Neuronales).
- **Fundamento Teórico**: (Ej. Mejor manejo de datos tabulares heterogéneos, invariancia ante transformaciones monótonas, eficiencia en árboles de decisión con histogramas).

---

## 2. Justificación de la Función de Pérdida y Métricas
- **Decisión**: (Ej. Optimizar por PR-AUC en vez de ROC-AUC).
- **Fundamento Teórico**: (Ej. En problemas con desbalance severo de clases, ROC-AUC puede presentar una visión optimista al verse amortiguado por el alto número de verdaderos negativos; PR-AUC se enfoca directamente en la precisión sobre la clase minoritaria).

---

## 3. Justificación del Esquema de Validación
- **Decisión**: (Ej. TimeSeriesSplit con ventana deslizante de 6 meses).
- **Fundamento Teórico**: (Ej. Evitar fugas de información temporal y reproducir fielmente el entorno de inferencia futura).
