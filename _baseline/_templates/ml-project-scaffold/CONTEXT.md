# CONTEXT.md — Arquitectura y Contratos: {{PROJECT_NAME}}

Este archivo define la estructura y contratos operativos del servicio de Machine Learning.

---

## 1. Mapa de Contexto

| Carpeta / Archivo | Tipo de Información | Cuándo consultarlo |
| :--- | :--- | :--- |
| `_context/api_specs.md` | Esquemas de solicitud/respuesta y rutas | Al modificar o agregar endpoints |
| `_context/architecture.md` | Arquitectura del pipeline, Docker y despliegue | Al modificar la infraestructura o flujo |
| `data/schemas/` | Contratos de validación (Pydantic / Pandera) | Al validar la calidad de datos de entrada |
| `src/pipeline/` | Scripts de ingesta, preprocesamiento y entrenamiento | Al ajustar el ciclo de entrenamiento |
| `src/inference/` | Carga de modelos y predicción optimizada | Al optimizar latencia o batching |
| `src/api/` | Controlador HTTP (FastAPI) | Al exponer modelos |
| `tests/` | Suites de tests unitarios y de integración | Antes de cualquier merge o commit |

---

## 2. Flujo de Trabajo
1. **Pipeline de Entrenamiento**: `src/pipeline/train.py` entrena el modelo, valida métricas mínimas y serializa artefactos a `models/registry/`.
2. **Servicio de Inferencia**: `src/api/main.py` levanta el servidor, carga el modelo serializado en el ciclo de vida de arranque y sirve predicciones vía HTTP POST.
3. **Calidad y Despliegue**: Se corren tests en `tests/` y se construye la imagen con `Dockerfile`.
