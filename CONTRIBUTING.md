# Guía de Contribución a `proyectosML`

¡Gracias por tu interés en contribuir a **proyectosML**! Este es un proyecto de código abierto diseñado para compartir una metodología rigurosa, reproducible y universal de desarrollo asistido por IA para Ciencia de Datos, Machine Learning y Sistemas Agénticos.

---

## 🎯 Principios de Contribución

Cualquier contribución (sea una nueva plantilla, una skill o una mejora al flujo) debe respetar los **10 Invariantes de ICM (Interpretable Context Methodology)**:

1. **Un folder, un trabajo**: Cada directorio debe tener un propósito único y explícito.
2. **Archivos de entrada ligeros**: `AGENTS.md` o `CLAUDE.md` deben ser routers de menos de 60 líneas.
3. **Numeración para secuencias**: Utilizar `01_`, `02_`, etc., cuando el orden de ejecución importe.
4. **Contratos explícitos (`CONTEXT.md`)**: Toda etapa debe definir qué lee (*inputs*), qué hace (*process*) y qué emite (*outputs*).
5. **Separación Fábrica vs. Producto**: Las reglas, plantillas y esquemas (estables) viven separados de los artefactos que genera cada ejecución.
6. **Cada salida es una superficie de edición**: Los artefactos intermedios deben ser legibles y editables por un humano antes de avanzar.
7. **Disciplina de tokens**: El contexto necesario por etapa debe mantenerse entre **2.000 y 8.000 tokens**.
8. **Texto plano y enlaces relativos**: Preferir Markdown, KaTeX y rutas relativas sobre formatos binarios o propietarios.
9. **El sistema de archivos es la máquina de estados**: El estado del proyecto se deduce inspeccionando los archivos presentes en el disco.
10. **Instanciación por copia**: Cada nuevo proyecto debe nacer copiando una plantilla de `_baseline/_templates/`, nunca de una hoja en blanco.

---

## 🛠️ ¿Cómo Contribuir?

### 1. Proponer un Nuevo Arquetipo de Proyecto
Si deseas añadir una nueva plantilla (por ejemplo: visión por computador, series de tiempo avanzadas o agentes con LangGraph):
1. Crea una carpeta en `_baseline/_templates/<nombre>-project-scaffold/`.
2. Incluye los adaptadores universales (`AGENTS.md`, `CLAUDE.md`, `.cursorrules`, `.windsurfrules`, `.github/copilot-instructions.md`).
3. Agrega la opción correspondiente en `init-project.sh`.
4. Documenta su propósito y estructura en `README.md`.

### 2. Flujo de Pull Request (PR)
1. Haz un Fork del repositorio: `https://github.com/f-marchant/proyectosML`.
2. Crea una rama para tu feature o corrección:
   ```bash
   git checkout -b feat/nueva-plantilla
   ```
3. Realiza tus cambios siguiendo **Conventional Commits**:
   - `feat:` Nueva funcionalidad o plantilla.
   - `fix:` Corrección de errores en scripts o configuraciones.
   - `docs:` Actualizaciones de documentación o citas.
4. Asegúrate de probar el script de inicialización:
   ```bash
   ./init-project.sh test-pr --type <tipo>
   ```
5. Envía un Pull Request describiendo claramente los cambios y cómo verificarlos.

---

## ⚖️ Licencia
Al contribuir a este repositorio, aceptas que tus contribuciones queden licenciadas bajo la misma [Licencia MIT](LICENSE) del proyecto.
