#!/usr/bin/env bash
# Participantes: [Jean Aquilla]
set -euo pipefail
destino="${1:-}"
if [[ -z "$destino" || "$destino" == -* ]]; then
  echo 'Uso: bash exercicio8/ping_rede.sh IP_DA_SUA_REDE' >&2
  exit 1
fi
# Quatro pedidos IPv4 facilitam associar sequência, resposta e RTT.
ping -4 -n -c 4 -W 3 "$destino"
