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

echo "🔗 [Antigravity] Registrando skills de línea base en ~/.gemini/config/skills/..."
for skill_path in "${BASE_DIR}/_baseline/skills"/*; do
    if [[ -d "${skill_path}" ]]; then
        skill_name="$(basename "${skill_path}")"
        rm -rf "${GEMINI_SKILLS_DIR}/${skill_name}"
        ln -sf "${skill_path}" "${GEMINI_SKILLS_DIR}/${skill_name}"
        echo "   -> ${skill_name}"
    fi
done

# 2. Configuración para Claude Code (~/.claude/skills)
CLAUDE_DIR="${HOME}/.claude"
CLAUDE_SKILLS_DIR="${CLAUDE_DIR}/skills"
mkdir -p "${CLAUDE_SKILLS_DIR}"

echo "🔗 [Claude Code] Registrando skills en ~/.claude/skills/..."
for skill_path in "${BASE_DIR}/_baseline/skills"/*; do
    if [[ -d "${skill_path}" ]]; then
        skill_name="$(basename "${skill_path}")"
        rm -rf "${CLAUDE_SKILLS_DIR}/${skill_name}"
        ln -sf "${skill_path}" "${CLAUDE_SKILLS_DIR}/${skill_name}"
    fi
done

# 3. Asegurar permisos ejecutables en scripts
chmod +x "${BASE_DIR}/init-project.sh"
chmod +x "${BASE_DIR}/bootstrap.sh"
if [[ -f "${BASE_DIR}/sync-adapters.sh" ]]; then
    chmod +x "${BASE_DIR}/sync-adapters.sh"
    echo "🔄 Sincronizando adaptadores de asistentes en la raíz..."
    bash "${BASE_DIR}/sync-adapters.sh" "${BASE_DIR}"
fi

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
echo "🎉 ¡Configuración de entorno proyectosML completada con éxito!"
echo "=================================================================="
echo "Alcance de la configuración:"
echo "  • Nivel Sistema / CLI:"
echo "    - Google Antigravity : ~/.gemini/config/GEMINI.md + skills globales"
echo "    - Claude Code (CLI)  : ~/.claude/skills/ (icm-architect, project-scaffold)"
echo "  • Nivel Workspace / Proyecto (vía sync-adapters.sh):"
echo "    - Cursor IDE         : .cursor/rules/main.mdc y .cursorrules"
echo "    - Windsurf / Cascade : .windsurfrules"
echo "    - GitHub Copilot     : .github/copilot-instructions.md"
echo "    - Claude Code        : CLAUDE.md"
echo ""
echo "Para crear un nuevo proyecto estandarizado ejecuta:"
echo "  cd ${BASE_DIR} && ./init-project.sh <nombre> --type <ds|ml|agentic|app>"
echo "=================================================================="
