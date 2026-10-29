#!/usr/bin/env bash
# ==============================================================================
# sync-adapters.sh — Generador y Sincronizador de Adaptadores de IA
# Single Source of Truth: Genera los adaptadores a partir de AGENTS.md y CONTEXT.md
# ==============================================================================

set -euo pipefail

TARGET_DIR="${1:-.}"
TARGET_DIR="$(cd "${TARGET_DIR}" && pwd)"

AGENTS_FILE="${TARGET_DIR}/AGENTS.md"
CONTEXT_FILE="${TARGET_DIR}/CONTEXT.md"

if [[ ! -f "${AGENTS_FILE}" ]]; then
    echo "❌ Error: No se encontró '${AGENTS_FILE}'. Este script debe ejecutarse en la raíz del repositorio o dentro de un proyecto." >&2
    exit 1
fi

PROJECT_NAME="$(basename "${TARGET_DIR}")"
echo "🔄 Sincronizando adaptadores de IA para '${PROJECT_NAME}' en ${TARGET_DIR}..."

# 1. Generar CLAUDE.md (Claude Code CLI)
cat <<EOF > "${TARGET_DIR}/CLAUDE.md"
# CLAUDE.md — ${PROJECT_NAME}

> Adaptador generado automáticamente por sync-adapters.sh a partir de AGENTS.md.

## Directrices y Reglas
- Reglas canónicas del proyecto: Consulta [AGENTS.md](AGENTS.md)
- Contratos de etapa y mapa de contexto: Consulta [CONTEXT.md](CONTEXT.md)

## Disciplina de Contexto
- Mantén el presupuesto entre 2.000 y 8.000 tokens por interacción.
- Consulta los archivos de '_context/' y 'research/' antes de escribir código.
EOF
echo "  ✅ CLAUDE.md sincronizado"

# 2. Generar .cursorrules (Cursor Legacy)
cat <<EOF > "${TARGET_DIR}/.cursorrules"
# Cursor Rules — ${PROJECT_NAME}
# Generated automatically by sync-adapters.sh from AGENTS.md

1. Always read AGENTS.md and CONTEXT.md before proposing or applying code changes.
2. Adhere to data inmutability conventions in data/raw/.
3. In Data Science projects, consult research/01_problem_formulation.md for theoretical formulas.
4. Prevent data leakage: all scalers and encoders must fit ONLY on the training split.
5. Fix random seeds to seed=42 across all libraries.
EOF
echo "  ✅ .cursorrules (Cursor legacy) sincronizado"

# 3. Generar .cursor/rules/main.mdc (Cursor Modern Rules)
mkdir -p "${TARGET_DIR}/.cursor/rules"
cat <<EOF > "${TARGET_DIR}/.cursor/rules/main.mdc"
---
description: Universal project guidelines and ICM contracts
globs: *
alwaysApply: true
---
# Main Project Directives — ${PROJECT_NAME}

Authoritative source of truth:
- Read [AGENTS.md](../../AGENTS.md) for coding standards, YAGNI, and security.
- Read [CONTEXT.md](../../CONTEXT.md) for stage contracts and file routing.
- If working with data, enforce data leakage prevention (fit on train only).
- Keep context lean (2k-8k tokens).
EOF
echo "  ✅ .cursor/rules/main.mdc (Cursor modern) sincronizado"

# 4. Generar .windsurfrules (Windsurf / Cascade)
cat <<EOF > "${TARGET_DIR}/.windsurfrules"
# Windsurf Rules — ${PROJECT_NAME}
# Generated automatically by sync-adapters.sh from AGENTS.md

1. Read AGENTS.md for engineering rules and CONTEXT.md for task contracts.
2. Maintain context discipline: read _context/ and research/ instead of scanning massive raw data.
3. Respect data immutability in data/raw/.
EOF
echo "  ✅ .windsurfrules (Windsurf) sincronizado"

# 5. Generar .github/copilot-instructions.md (GitHub Copilot)
mkdir -p "${TARGET_DIR}/.github"
cat <<EOF > "${TARGET_DIR}/.github/copilot-instructions.md"
# GitHub Copilot Instructions — ${PROJECT_NAME}
<!-- Generated automatically by sync-adapters.sh from AGENTS.md -->

- Authoritative source: refer to AGENTS.md for development standards and CONTEXT.md for stage contracts.
- In data science workflows, ensure scalers and encoders are fitted only on training data.
- Reproducibility: enforce random_state=42 across all ML pipelines.
EOF
echo "  ✅ .github/copilot-instructions.md (Copilot) sincronizado"

echo "🎉 ¡Todos los adaptadores de IA están sincronizados con AGENTS.md!"
