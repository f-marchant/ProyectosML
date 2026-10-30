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

## 2. Enrutamiento Rápido de Tareas y Skills Disponibles

- **Para crear un nuevo proyecto**: Ejecuta `./init-project.sh <nombre> --type <ds|ml|agentic>` o invoca la skill `project-scaffold`.
- **Para consultar proyectos activos**: Lee `CONTEXT.md` en la raíz.
- **Para auditar o diseñar un nuevo flujo ICM**: Invoca la skill `icm-architect`.
- **Para desafiar y validar un plan/diseño antes de codificar**: Invoca la skill `grill-me`.
- **Para depurar fallos o regresiones sistemáticamente**: Invoca la skill `diagnose`.
- **Para compactar y transferir la sesión actual**: Invoca la skill `handoff`.
- **Para retrospectiva y mejora de directrices/guardarraíles**: Invoca la skill `retro`.
- **Para proyectos agénticos (`--type agentic`)**: Disponen de las skills especializadas `to-spec`, `to-tickets` e `implement-spec` en `.agents/skills/`.
- **Para trabajar en un proyecto específico**: Abre el directorio del proyecto en `projects/<nombre>/`.

---

## 3. Disciplina de Contexto
- Nunca intentes cargar todos los proyectos a la vez. Cuando trabajes en un proyecto dentro de `projects/`, enfócate exclusivamente en sus archivos locales y su `CONTEXT.md`.
- Mantén la disciplina de 2.000 a 8.000 tokens por interacción.
