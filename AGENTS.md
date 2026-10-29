# AGENTS.md — Espacio Privado: workspace_proyectos

> **Espacio Umbrella Privado**: Proyectos personales y de trabajo (Confidencial).
> **Framework Base**: [ProyectosML](https://github.com/f-marchant/ProyectosML) (Interpretable Context Methodology - ICM).
> **Autor**: @f-marchant

---

## 1. Dónde estoy y Qué rige este Workspace Privado

Este es tu espacio de desarrollo privado bajo la metodología **ICM (Interpretable Context Methodology)**:
- **`projects/`**: Espacio exclusivo donde residen tus proyectos personales y laborales.
- **`_baseline/`**: Fábrica local de plantillas (`ds`, `ml`, `agentic`) y skills de soporte.
- **`init-project.sh`**: Script para instanciar proyectos en 1 segundo con adaptadores para cualquier IA.
- **`bootstrap.sh`**: Instalador de la línea base en Antigravity y Claude Code.

---

## 2. Restricciones y Confidencialidad
1. **Privacidad Estricta**: Este repositorio es estrictamente confidencial. Jamás filtres datos de clientes o llaves a entornos públicos.
2. **Inmutabilidad y Calidad**: Toda manipulación de datos en `data/raw/` de cualquier subproyecto es de solo lectura.
3. **Disciplina de Tokens**: No leas datasets masivos; consulta `_context/domain.md` y `CONTEXT.md` de cada subproyecto.
4. **Sustento Teórico**: En proyectos de Ciencia de Datos (`--type ds`), documenta la formulación matemática e hipótesis en `research/`.

---

## 3. Comandos Rápidos
- Crear nuevo proyecto: `./init-project.sh <nombre> --type <ds|ml|agentic>`
- Sincronizar mejoras de la línea base pública: `git pull upstream main`
