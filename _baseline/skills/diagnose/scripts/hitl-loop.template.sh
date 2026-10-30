#!/usr/bin/env bash
# Human-in-the-loop (HITL) reproduction loop.
# Plantilla para capturar confirmaciones del usuario en diagnósticos complejos.
#
# Uso:
#   bash scripts/hitl-loop.template.sh
#

set -euo pipefail

step() {
  printf '\n>>> %s\n' "$1"
  read -r -p "    [Presiona Enter al completar el paso] " _
}

capture() {
  local var="$1" question="$2" answer
  printf '\n>>> %s\n' "$question"
  read -r -p "    > " answer
  printf -v "$var" '%s' "$answer"
}

# --- Edita los pasos a continuación ------------------------------------------

step "Inicia el servicio o script objetivo en la terminal correspondiente."

capture ERRORED "¿Se produjo el fallo o excepción observada? (s/n)"

capture ERROR_MSG "Pega aquí el mensaje o traza del error (o 'ninguno'):"

# ------------------------------------------------------------------------------

printf '\n--- Resultados Capturados ---\n'
printf 'ERRORED=%s\n' "$ERRORED"
printf 'ERROR_MSG=%s\n' "$ERROR_MSG"
