#!/usr/bin/env bash
# ==============================================================================
# sync-upstream.sh — Sincronizador Seguro de Arquitectura Base a Repositorio Público
# Repositorio Público: ProyectosML (upstream)
# Repositorio Privado: workspace_proyectos (origin)
# ==============================================================================
# Regla de Seguridad: NUNCA sincroniza la carpeta 'projects/' con el repositorio
# público upstream. Solo replica mejoras a la arquitectura base (_baseline/,
# scripts, templates, directrices y documentación) previa confirmación del usuario.
# ==============================================================================

set -euo pipefail

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
UPSTREAM_REMOTE="upstream"
PUBLIC_BRANCH="upstream-release"
CURRENT_BRANCH="$(git rev-parse --abbrev-ref HEAD)"

echo "=================================================================="
echo "🛡️  Sincronización Segura hacia Repositorio Público (ProyectosML)"
echo "=================================================================="

# 1. Verificar que existe el remoto upstream
if ! git remote get-url "${UPSTREAM_REMOTE}" >/dev/null 2>&1; then
    echo "❌ Error: No se encontró el remoto '${UPSTREAM_REMOTE}'." >&2
    exit 1
fi

UPSTREAM_URL="$(git remote get-url "${UPSTREAM_REMOTE}")"
echo "📍 Remoto destino: ${UPSTREAM_REMOTE} (${UPSTREAM_URL})"

# 2. Verificar que el árbol de trabajo esté limpio
if [[ -n "$(git status --porcelain)" ]]; then
    echo "⚠️  Tienes cambios pendientes en tu espacio de trabajo." >&2
    echo "   Por favor confirma o descarta tus cambios antes de sincronizar con upstream." >&2
    exit 1
fi

# 3. Asegurar que estamos en main
if [[ "${CURRENT_BRANCH}" != "main" ]]; then
    echo "⚠️  Debes estar en la rama 'main' para sincronizar con upstream." >&2
    exit 1
fi

echo "🔄 Obteniendo estado actualizado de ${UPSTREAM_REMOTE}..."
git fetch "${UPSTREAM_REMOTE}" main >/dev/null 2>&1 || true

# 4. Crear o resetear la rama de publicación limpia (upstream-release)
echo "🧹 Preparando árbol de publicación limpio (excluyendo 'projects/')..."
git checkout -B "${PUBLIC_BRANCH}" main >/dev/null 2>&1

# 5. Aplicar exclusión estricta de proyectos personales en la rama de publicación
# Mantener solo projects/.gitkeep
if [[ -d "${BASE_DIR}/projects" ]]; then
    find "${BASE_DIR}/projects" -mindepth 1 -maxdepth 1 ! -name ".gitkeep" -exec rm -rf {} +
fi

# Sanitizar CONTEXT.md para eliminar líneas de proyectos personales
if [[ -f "${BASE_DIR}/CONTEXT.md" ]]; then
    # Filtrar cualquier fila de la tabla que apunte a projects/ excepto la descripción general
    awk '
    BEGIN { in_projects = 0 }
    /^\| `.*` \|/ {
        if ($0 ~ /`projects\// && $0 !~ /Layer 4/) {
            next
        }
    }
    { print }
    ' "${BASE_DIR}/CONTEXT.md" > "${BASE_DIR}/CONTEXT.md.tmp" && mv "${BASE_DIR}/CONTEXT.md.tmp" "${BASE_DIR}/CONTEXT.md"
fi

# Verificar si hay cambios tras la limpieza
git add -A projects/ CONTEXT.md >/dev/null 2>&1 || true

if ! git diff --cached --quiet; then
    git commit -m "chore(sync): aislar arquitectura base excluyendo proyectos personales" >/dev/null 2>&1
fi

# 6. Comparar contra upstream/main
UPSTREAM_COMMIT="$(git rev-parse "${UPSTREAM_REMOTE}/main" 2>/dev/null || echo "")"
CHANGES_COUNT=0

if [[ -n "${UPSTREAM_COMMIT}" ]]; then
    CHANGES_COUNT="$(git rev-list --count "${UPSTREAM_REMOTE}/main..${PUBLIC_BRANCH}" 2>/dev/null || echo "0")"
fi

echo ""
echo "🔍 Comparando arquitectura base contra ${UPSTREAM_REMOTE}/main:"

if [[ "${CHANGES_COUNT}" -eq 0 && -n "${UPSTREAM_COMMIT}" && "$(git diff "${UPSTREAM_REMOTE}/main..${PUBLIC_BRANCH}" --stat | wc -l)" -eq 0 ]]; then
    echo "✅ El repositorio público ProyectosML ya está al día con la arquitectura base."
    git checkout main >/dev/null 2>&1
    git branch -D "${PUBLIC_BRANCH}" >/dev/null 2>&1 || true
    echo "=================================================================="
    exit 0
fi

echo "Archivos que se sincronizarán con ProyectosML (excluyendo 'projects/'):"
echo "──────────────────────────────────────────────────────────────────"
git diff --stat "${UPSTREAM_REMOTE}/main..${PUBLIC_BRANCH}" | grep -v "projects/" || true
echo "──────────────────────────────────────────────────────────────────"

# 7. Verificación de seguridad de proyectos
if git diff --name-only "${UPSTREAM_REMOTE}/main..${PUBLIC_BRANCH}" | grep "^projects/" | grep -v "projects/\.gitkeep"; then
    echo "❌ ERROR CRÍTICO DE SEGURIDAD: Se detectaron archivos en projects/ dentro del paquete de sincronización." >&2
    echo "   Abortando inmediatamente para proteger la privacidad." >&2
    git checkout main >/dev/null 2>&1
    git branch -D "${PUBLIC_BRANCH}" >/dev/null 2>&1 || true
    exit 1
fi

# 8. Confirmación obligatoria del usuario
echo ""
CONFIRM=""
if [[ "${1:-}" == "--yes" || "${1:-}" == "-y" ]]; then
    CONFIRM="s"
else
    read -r -p "¿Confirmas la sincronización de estos cambios hacia el repositorio público ProyectosML (upstream)? [s/N]: " CONFIRM
fi

if [[ "${CONFIRM}" =~ ^[sS]$ ]]; then
    echo "🚀 Sincronizando con ${UPSTREAM_REMOTE}/main..."
    git push "${UPSTREAM_REMOTE}" "${PUBLIC_BRANCH}:main"
    echo ""
    echo "🎉 ¡Sincronización completada con éxito!"
    echo "   El repositorio público ProyectosML ha sido actualizado con la arquitectura base."
    echo "   La carpeta 'projects/' permanece 100% privada y fuera de upstream."
else
    echo "⏸️  Sincronización cancelada por el usuario."
fi

# 9. Regresar a la rama main
git checkout main >/dev/null 2>&1
git branch -D "${PUBLIC_BRANCH}" >/dev/null 2>&1 || true
echo "=================================================================="
