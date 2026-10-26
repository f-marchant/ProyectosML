# Guía de Recuperación y Configuración en Nuevo Equipo Personal

> **Propósito**: Permitir la reconstrucción total e inmediata de tu entorno de desarrollo `proyectosML` y su sincronización con Google Antigravity en caso de migrar o formatear tu equipo.

---

## 📋 Requisitos Previos en la Nueva Máquina

Antes de comenzar, asegúrate de tener instalados en tu sistema operativo:
1. **Git**:
   - Fedora/RHEL: `sudo dnf install git`
   - Ubuntu/Debian: `sudo apt install git`
   - macOS: `brew install git`
2. **Python 3.10+**:
   - Con soporte para `pip` y entornos virtuales (`venv`).
3. **Google Antigravity**:
   - Instalado y con sesión iniciada.
4. **Acceso a tu cuenta de GitHub**:
   - Clave SSH configurada o Personal Access Token (PAT).

---

## ⚡ Procedimiento de Reconstrucción en 3 Pasos

### Paso 1: Clonar el Repositorio
Abre tu terminal en el directorio raíz de usuario (`~` o `/home/usuario`):

```bash
cd ~
git clone https://github.com/f-marchant/proyectosML.git
cd proyectosML
```

### Paso 2: Ejecutar el Script de Bootstrap
Ejecuta el script de automatización:

```bash
chmod +x bootstrap.sh
./bootstrap.sh
```

**¿Qué hace `bootstrap.sh` automáticamente?**
1. Crea la estructura de configuración de Antigravity en `~/.gemini/config/`.
2. Vincula mediante enlace simbólico (`symlink`) la regla global `_baseline/global_config/GEMINI.md` a `~/.gemini/config/GEMINI.md`.
3. Registra las skills globales:
   - `~/.gemini/config/skills/icm-architect`
   - `~/.gemini/config/skills/project-scaffold`
4. Asegura permisos de ejecución para `init-project.sh`.

### Paso 3: Validar en Antigravity
Abre Antigravity en el directorio `~/proyectosML/`:
- El agente detectará automáticamente la regla global y la estructura Umbrella.
- Para verificar que la skill `icm-architect` está activa, puedes preguntar al agente:
  *"¿Qué arquetipos de ICM tienes disponibles?"*
  El agente responderá describiendo los 6 arquetipos de RinDig (Pipeline, Umbrella, Record Library, etc.).

---

## 🛠️ Herramientas Complementarias Recomendadas

Para un flujo óptimo de formateo y validación de código:
```bash
# Formateador ultra-rápido (utilizado por los hooks de los proyectos)
pip install --user ruff pytest
```

---

## 🔄 Actualización de la Línea Base en el Futuro

Cualquier mejora que hagas a las plantillas o reglas en tu máquina:
1. Se edita dentro de `_baseline/`.
2. Se versiona con Git:
   ```bash
   git add _baseline/
   git commit -m "feat(baseline): actualizar plantilla de ciencia de datos con nuevas métricas"
   git push origin main
   ```
3. En cualquier otra máquina personal, basta con ejecutar:
   ```bash
   git pull origin main
   ./bootstrap.sh
   ```
¡Tu entorno estará permanentemente sincronizado y respaldado!
