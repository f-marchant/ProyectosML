#!/usr/bin/env bash
# ==============================================================================
# bootstrap.sh — Instalador de Línea Base y Recuperación ante Cambio de Equipo
# Espacio de Trabajo: proyectosML
# ==============================================================================

set -euo pipefail

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GEMINI_CONFIG_DIR="${HOME}/.gemini/config"
GEMINI_SKILLS_DIR="${GEMINI_CONFIG_DIR}/skills"

echo "=================================================================="
echo "🛠️  Iniciando Bootstrap de Línea Base proyectosML..."
echo "=================================================================="

# 1. Asegurar directorios de configuración de Antigravity
mkdir -p "${GEMINI_CONFIG_DIR}"
mkdir -p "${GEMINI_SKILLS_DIR}"

# 2. Configurar Regla Global (~/.gemini/config/GEMINI.md)
GLOBAL_RULE_SRC="${BASE_DIR}/_baseline/global_config/GEMINI.md"
GLOBAL_RULE_DEST="${GEMINI_CONFIG_DIR}/GEMINI.md"

if [[ -f "${GLOBAL_RULE_DEST}" ]]; then
    echo "ℹ️  Respaldando regla global existente en GEMINI.md.bak..."
    cp "${GLOBAL_RULE_DEST}" "${GLOBAL_RULE_DEST}.bak"
fi

echo "🔗 Vinculando regla global GEMINI.md..."
ln -sf "${GLOBAL_RULE_SRC}" "${GLOBAL_RULE_DEST}"

# 3. Instalar / Enlazar Skills Globales
echo "🔗 Registrando skill 'icm-architect'..."
rm -rf "${GEMINI_SKILLS_DIR}/icm-architect"
ln -sf "${BASE_DIR}/_baseline/skills/icm-architect" "${GEMINI_SKILLS_DIR}/icm-architect"

echo "🔗 Registrando skill 'project-scaffold'..."
rm -rf "${GEMINI_SKILLS_DIR}/project-scaffold"
ln -sf "${BASE_DIR}/_baseline/skills/project-scaffold" "${GEMINI_SKILLS_DIR}/project-scaffold"

# 4. Asegurar permisos ejecutables en scripts
chmod +x "${BASE_DIR}/init-project.sh"
chmod +x "${BASE_DIR}/bootstrap.sh"

# 5. Comprobar herramientas recomendadas
echo ""
echo "🔍 Verificando herramientas del sistema:"
command -v git >/dev/null 2>&1 && echo "  ✅ git: detectado" || echo "  ⚠️  git: NO instalado"
command -v python3 >/dev/null 2>&1 && echo "  ✅ python3: detectado" || echo "  ⚠️  python3: NO instalado"
command -v ruff >/dev/null 2>&1 && echo "  ✅ ruff: detectado" || echo "  ℹ️  ruff: no detectado en PATH (recomendado para formateo rápido: pip install ruff)"

echo ""
echo "=================================================================="
echo "🎉 ¡Línea base de proyectosML instalada con éxito!"
echo "=================================================================="
echo "Antigravity ahora tiene activas:"
echo "  • Reglas globales de calidad y metodología ICM en ~/.gemini/config/GEMINI.md"
echo "  • Skill global 'icm-architect' (para diseñar y auditar workspaces)"
echo "  • Skill global 'project-scaffold' (para crear proyectos por chat)"
echo ""
echo "Para crear un nuevo proyecto ejecuta:"
echo "  cd ${BASE_DIR} && ./init-project.sh <nombre> --type <ds|ml|agentic>"
echo "=================================================================="
