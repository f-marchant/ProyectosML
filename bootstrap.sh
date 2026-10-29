#!/usr/bin/env bash
# ==============================================================================
# bootstrap.sh — Instalador Universal de Línea Base (Antigravity, Claude Code, Cursor, Windsurf)
# Espacio de Trabajo: proyectosML
# ==============================================================================

set -euo pipefail

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GLOBAL_RULE_SRC="${BASE_DIR}/_baseline/global_config/GEMINI.md"

echo "=================================================================="
echo "🛠️  Iniciando Bootstrap Universal de Línea Base proyectosML..."
echo "=================================================================="

# 1. Configuración para Google Antigravity
GEMINI_CONFIG_DIR="${HOME}/.gemini/config"
GEMINI_SKILLS_DIR="${GEMINI_CONFIG_DIR}/skills"
mkdir -p "${GEMINI_CONFIG_DIR}" "${GEMINI_SKILLS_DIR}"

if [[ -f "${GEMINI_CONFIG_DIR}/GEMINI.md" && ! -L "${GEMINI_CONFIG_DIR}/GEMINI.md" ]]; then
    echo "ℹ️  Respaldando regla global existente en GEMINI.md.bak..."
    cp "${GEMINI_CONFIG_DIR}/GEMINI.md" "${GEMINI_CONFIG_DIR}/GEMINI.md.bak"
fi

echo "🔗 [Antigravity] Vinculando regla global GEMINI.md..."
ln -sf "${GLOBAL_RULE_SRC}" "${GEMINI_CONFIG_DIR}/GEMINI.md"

echo "🔗 [Antigravity] Registrando skills 'icm-architect' y 'project-scaffold'..."
rm -rf "${GEMINI_SKILLS_DIR}/icm-architect" "${GEMINI_SKILLS_DIR}/project-scaffold"
ln -sf "${BASE_DIR}/_baseline/skills/icm-architect" "${GEMINI_SKILLS_DIR}/icm-architect"
ln -sf "${BASE_DIR}/_baseline/skills/project-scaffold" "${GEMINI_SKILLS_DIR}/project-scaffold"

# 2. Configuración para Claude Code (~/.claude/skills)
CLAUDE_DIR="${HOME}/.claude"
CLAUDE_SKILLS_DIR="${CLAUDE_DIR}/skills"
mkdir -p "${CLAUDE_SKILLS_DIR}"

echo "🔗 [Claude Code] Registrando skills en ~/.claude/skills/..."
rm -rf "${CLAUDE_SKILLS_DIR}/icm-architect" "${CLAUDE_SKILLS_DIR}/project-scaffold"
ln -sf "${BASE_DIR}/_baseline/skills/icm-architect" "${CLAUDE_SKILLS_DIR}/icm-architect"
ln -sf "${BASE_DIR}/_baseline/skills/project-scaffold" "${CLAUDE_SKILLS_DIR}/project-scaffold"

# 3. Asegurar permisos ejecutables en scripts
chmod +x "${BASE_DIR}/init-project.sh"
chmod +x "${BASE_DIR}/bootstrap.sh"

# 4. Comprobar herramientas instaladas en el sistema
echo ""
echo "🔍 Verificando herramientas de desarrollo e IA:"
command -v git >/dev/null 2>&1 && echo "  ✅ git: detectado" || echo "  ⚠️  git: NO instalado"
command -v python3 >/dev/null 2>&1 && echo "  ✅ python3: detectado" || echo "  ⚠️  python3: NO instalado"
command -v ruff >/dev/null 2>&1 && echo "  ✅ ruff: detectado" || echo "  ℹ️  ruff: no detectado (recomendado: pip install ruff)"
command -v claude >/dev/null 2>&1 && echo "  ✅ claude (Claude Code CLI): detectado" || echo "  ℹ️  claude: no detectado en PATH"
command -v cursor >/dev/null 2>&1 && echo "  ✅ cursor: detectado" || echo "  ℹ️  cursor: no detectado en PATH"

echo ""
echo "=================================================================="
echo "🎉 ¡Línea base universal de proyectosML instalada con éxito!"
echo "=================================================================="
echo "Herramientas de IA configuradas con la misma línea base:"
echo "  • Google Antigravity : ~/.gemini/config/GEMINI.md + skills globales"
echo "  • Claude Code (CLI)  : ~/.claude/skills/ + CLAUDE.md"
echo "  • Cursor IDE         : .cursorrules en cada proyecto"
echo "  • Windsurf / Cascade : .windsurfrules en cada proyecto"
echo "  • GitHub Copilot     : .github/copilot-instructions.md en cada proyecto"
echo ""
echo "Para crear un nuevo proyecto compatible con cualquier IA ejecuta:"
echo "  cd ${BASE_DIR} && ./init-project.sh <nombre> --type <ds|ml|agentic>"
echo "=================================================================="
