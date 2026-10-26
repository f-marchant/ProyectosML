#!/usr/bin/env bash
# ==============================================================================
# init-project.sh — Generador Automatizado de Proyectos para proyectosML
# Metodología: ICM (Interpretable Context Methodology) + Antigravity
# ==============================================================================

set -euo pipefail

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATES_DIR="${BASE_DIR}/_baseline/_templates"
PROJECTS_DIR="${BASE_DIR}/projects"
ROOT_CONTEXT="${BASE_DIR}/CONTEXT.md"

usage() {
    cat <<EOF
Uso: $0 <nombre-proyecto> [--type ds|ml|agentic] ["Descripción breve del proyecto"]

Tipos de proyecto disponibles:
  ds        Ciencia de Datos (CRISP-DM + research/ + capas de datos + notebooks) [DEFAULT]
  ml        Machine Learning Productivo (API FastAPI + Docker + pipelines)
  agentic   Desarrollo Agéntico (Prompts + Tools/MCP + Evals + Grafos de estado)

Ejemplos:
  $0 churn-prediction --type ds "Modelo predictivo de fuga de clientes con lightgbm"
  $0 recommendation-api --type ml "Microservicio de recomendaciones en tiempo real"
  $0 research-agent --type agentic "Asistente autónomo con herramientas de búsqueda"
EOF
    exit 1
}

if [[ $# -lt 1 ]]; then
    usage
fi

PROJECT_NAME="$1"
shift

PROJECT_TYPE="ds"
PROJECT_DESC=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --type)
            PROJECT_TYPE="$2"
            shift 2
            ;;
        -h|--help)
            usage
            ;;
        *)
            if [[ -z "${PROJECT_DESC}" ]]; then
                PROJECT_DESC="$1"
            fi
            shift
            ;;
    esac
done

if [[ -z "${PROJECT_DESC}" ]]; then
    PROJECT_DESC="Proyecto ${PROJECT_NAME} bajo metodología ICM"
fi

# Validar nombre
if [[ ! "${PROJECT_NAME}" =~ ^[a-z0-9-]+$ ]]; then
    echo "❌ Error: El nombre del proyecto debe contener solo letras minúsculas, números y guiones (-) (kebab-case)." >&2
    exit 1
fi

TARGET_DIR="${PROJECTS_DIR}/${PROJECT_NAME}"
if [[ -d "${TARGET_DIR}" ]]; then
    echo "❌ Error: El proyecto '${PROJECT_NAME}' ya existe en ${TARGET_DIR}." >&2
    exit 1
fi

case "${PROJECT_TYPE}" in
    ds)
        TEMPLATE_SOURCE="${TEMPLATES_DIR}/ds-project-scaffold"
        TYPE_LABEL="Ciencia de Datos"
        ;;
    ml)
        TEMPLATE_SOURCE="${TEMPLATES_DIR}/ml-project-scaffold"
        TYPE_LABEL="Machine Learning Productivo"
        ;;
    agentic)
        TEMPLATE_SOURCE="${TEMPLATES_DIR}/agentic-project-scaffold"
        TYPE_LABEL="Desarrollo Agéntico"
        ;;
    *)
        echo "❌ Error: Tipo de proyecto no reconocido: '${PROJECT_TYPE}'." >&2
        echo "Opciones válidas: ds | ml | agentic" >&2
        exit 1
        ;;
esac

if [[ ! -d "${TEMPLATE_SOURCE}" ]]; then
    echo "❌ Error: No se encontró la plantilla en ${TEMPLATE_SOURCE}." >&2
    exit 1
fi

echo "🚀 Creando nuevo proyecto '${PROJECT_NAME}' [Tipo: ${TYPE_LABEL}]..."

# 1. Copiar plantilla completa respetando archivos ocultos
cp -r "${TEMPLATE_SOURCE}" "${TARGET_DIR}"

# 2. Reemplazar placeholders en archivos de contexto y documentación
CREATION_DATE="$(date +'%Y-%m-%d')"

# Detectar SO para sintaxis de sed
if [[ "$OSTYPE" == "darwin"* ]]; then
    SED_INPLACE=("sed" "-i" "")
else
    SED_INPLACE=("sed" "-i")
fi

find "${TARGET_DIR}" -type f -name "*.md" -exec "${SED_INPLACE[@]}" "s/{{PROJECT_NAME}}/${PROJECT_NAME}/g" {} +
find "${TARGET_DIR}" -type f -name "*.md" -exec "${SED_INPLACE[@]}" "s/{{PROJECT_DESCRIPTION}}/${PROJECT_DESC}/g" {} +
find "${TARGET_DIR}" -type f -name "*.md" -exec "${SED_INPLACE[@]}" "s/{{CREATION_DATE}}/${CREATION_DATE}/g" {} +

# 3. Registrar el proyecto en el catálogo raíz (CONTEXT.md)
if [[ -f "${ROOT_CONTEXT}" ]]; then
    if ! grep -q "projects/${PROJECT_NAME}" "${ROOT_CONTEXT}"; then
        echo "| \`${PROJECT_NAME}\` | ${TYPE_LABEL} | \`projects/${PROJECT_NAME}/\` | ${PROJECT_DESC} |" >> "${ROOT_CONTEXT}"
    fi
fi

cat <<EOF

✅ ¡Proyecto '${PROJECT_NAME}' creado exitosamente!
─────────────────────────────────────────────────────────────
📂 Ubicación: ${TARGET_DIR}
🏷️  Tipo:      ${TYPE_LABEL} (${PROJECT_TYPE})
📄 Resumen:   ${PROJECT_DESC}
─────────────────────────────────────────────────────────────

Próximos pasos recomendados:
  1. cd ${TARGET_DIR}
  2. Revisa y completa 'research/01_problem_formulation.md' o '_context/domain.md'
  3. Abre una sesión con Antigravity para comenzar el desarrollo guiado por contratos ICM.
EOF
