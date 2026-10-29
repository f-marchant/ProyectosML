# AGENTS.md — Espacio de Trabajo: proyectosML

> **Espacio Umbrella**: Colección de Proyectos de Ciencia de Datos, Machine Learning y Sistemas Agénticos.
> **Autor**: @f-marchant
> **Repositorio**: https://github.com/f-marchant/proyectosML

---

## 1. Dónde estoy y Cómo funciona este Repositorio (Patrón Umbrella)

Este repositorio es un **Paraguas de Proyectos (Umbrella Workspace)** estructurado bajo la metodología **ICM (Interpretable Context Methodology)**:
- **`_baseline/`**: La fábrica portable y reproducible (reglas globales, skills y plantillas de andamiaje).
- **`projects/`**: Directorio donde residen los proyectos individuales e independientes.
- **`init-project.sh`**: Script para instanciar nuevos proyectos en segundos con sus contratos de contexto.
- **`bootstrap.sh`**: Script de autoconfiguración de Antigravity para este o cualquier equipo nuevo.

---

## 2. Enrutamiento Rápido de Tareas

- **Para crear un nuevo proyecto**: Ejecuta `./init-project.sh <nombre> --type <ds|ml|agentic>`.
- **Para consultar proyectos activos**: Lee `CONTEXT.md` en la raíz.
- **Para auditar o diseñar un nuevo flujo**: Invoca la skill `icm-architect`.
- **Para trabajar en un proyecto específico**: Abre el directorio del proyecto en `projects/<nombre>/`.

---

## 3. Disciplina de Contexto
- Nunca intentes cargar todos los proyectos a la vez. Cuando trabajes en un proyecto dentro de `projects/`, enfócate exclusivamente en sus archivos locales y su `CONTEXT.md`.
- Mantén la disciplina de 2.000 a 8.000 tokens por interacción.
