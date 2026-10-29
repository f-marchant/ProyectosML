# Especificación de API y Contratos de Datos: {{PROJECT_NAME}}

## 1. Endpoints de la API

### `POST /predict`
- **Descripción**: Recibe un vector de características y retorna la predicción con su nivel de confianza.
- **Payload Request**:
  ```json
  {
    "features": {
      "feature_a": 12.5,
      "feature_b": "categoria_x"
    }
  }
  ```
- **Payload Response**:
  ```json
  {
    "prediction": 1,
    "probability": 0.89,
    "model_version": "v1.0.0"
  }
  ```

### `GET /health`
- **Descripción**: Chequeo de salud del servicio y disponibilidad del modelo en memoria.
