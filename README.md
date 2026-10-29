# workspace_proyectos (Repositorio Privado)

Espacio de trabajo privado y confidencial para proyectos personales y de trabajo, gobernado por la metodología **ICM (Interpretable Context Methodology)** e impulsado por el marco de trabajo [ProyectosML](https://github.com/f-marchant/ProyectosML).

---

## 🔒 Confidencialidad y Propósito

Este repositorio es estrictamente **PRIVADO**. Contiene:
- Proyectos analíticos y de machine learning para el trabajo y uso personal.
- Código de producción, pipelines de datos e implementaciones de agentes.
- Toda la estructura hereda la línea base universal compatible con **Antigravity, Claude Code, Cursor, Windsurf y GitHub Copilot**.

---

## 🚀 Uso Rápido

### Crear un Nuevo Proyecto en este Espacio
```bash
# Ciencia de Datos (con research/ y capas de datos):
./init-project.sh mi-analisis --type ds "Objetivo del análisis"

# Machine Learning Productivo (API FastAPI + Docker):
./init-project.sh mi-api --type ml "Microservicio productivo"

# Desarrollo Agéntico (Prompts + Tools + Evals):
./init-project.sh mi-agente --type agentic "Agente autónomo"
```

---

## 🔄 Actualizar la Línea Base desde el Framework Público

Cuando actualices o mejores plantillas en tu repositorio público `ProyectosML`:
```bash
git fetch upstream
git merge upstream/main -m "chore: sincronizar mejoras de linea base publica"
```
*(Tus proyectos dentro de `projects/` no se verán alterados).*
