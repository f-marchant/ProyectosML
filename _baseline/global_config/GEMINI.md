# Global Antigravity Guidelines & Baseline Rules

Esta es la línea base de desarrollo universal para todos los proyectos en esta máquina.
Define la filosofía de ingeniería, estándares de calidad y disciplina de contexto.

---

## 1. Filosofía de Ingeniería y Modo de Trabajo

1. **Senior Developer / YAGNI (You Aren't Gonna Need It)**:
   - Resuelve el problema actual de la forma más limpia, directa y mantenible posible.
   - Evita la sobre-ingeniería, abstracciones prematuras y capas innecesarias.
   - No agregues librerías ni dependencias externas sin justificación técnica explícita.
2. **Seguridad y Acciones Destructivas**:
   - NUNCA ejecutes comandos destructivos (`rm -rf`, `DROP TABLE`, `git reset --hard`) sin confirmación explícita previa del usuario.
   - Jamás expongas credenciales, llaves privadas ni tokens en commits o logs.

---

## 2. Disciplina de Contexto (Metodología ICM)

1. **Carga Selectiva (Presupuesto de 2.000 a 8.000 tokens)**:
   - No intentes leer directorios enteros ni datasets completos (`.csv`, `.parquet`).
   - Consulta primero el archivo `CONTEXT.md` del proyecto o etapa actual para entender el contrato de entrada/salida.
   - Consulta `_context/domain.md` para el diccionario de datos y reglas de negocio, o `research/` para el sustento teórico.
2. **Superficie de Edición Humana**:
   - Cada entrega o reporte intermedio en markdown es una superficie que el usuario puede revisar y editar antes de pasar a la siguiente etapa.
   - Respeta siempre las decisiones que el usuario haya dejado consignadas en los archivos de salida.

---

## 3. Estándares para Ciencia de Datos y Machine Learning

1. **Inmutabilidad de Datos**:
   - Los datos en `data/raw/` son estrictamente de solo lectura. Todo procesamiento debe emitir a `data/interim/` o `data/processed/`.
2. **Prevención de Data Leakage**:
   - Todo escalado, imputación y codificación debe ajustarse (`fit`) exclusivamente sobre los datos de entrenamiento (`train`) y transformarse (`transform`) en validación/test.
   - En series de tiempo, respeta estrictamente el orden temporal (validación hacia adelante / *expanding window*).
3. **Reproducibilidad Rigurosa**:
   - Fija siempre semillas aleatorias (`seed=42` o la definida en `_context/conventions.md`) en numpy, pandas, torch, scikit-learn, etc.
   - Todo análisis debe poder ejecutarse de extremo a extremo sin depender del estado en memoria de un kernel interactivo.

---

## 4. Convenciones de Control de Versiones (Git)

1. **Conventional Commits**:
   - `feat:` Nueva funcionalidad o modelo.
   - `fix:` Corrección de errores o bugs.
   - `docs:` Documentación, notas teóricas o actualización de contratos.
   - `refactor:` Reestructuración de código sin alterar comportamiento.
   - `test:` Nuevos tests unitarios o datasets de evaluación.
   - `chore:` Tareas de mantenimiento, dependencias o configuración.
2. **Higiene de Repositorio**:
   - Nunca comitear pesos binarios gigantes (`*.pkl`, `*.pt`, `*.onnx`) ni datasets crudos al repositorio Git.
