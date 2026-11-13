#!/usr/bin/env bash
# Participantes: [Jean Aquilla]
set -euo pipefail
interface="${1:-}"
if [[ -z "$interface" || "$interface" == -* || ! -d "/sys/class/net/$interface" ]]; then
  echo 'Uso: sudo bash exercicio9/renovar_dhcp.sh INTERFACE' >&2
  exit 1
fi
if [[ "${EUID}" -ne 0 ]]; then echo 'Execute com sudo.' >&2; exit 1; fi
if ! command -v dhclient >/dev/null; then
  echo 'dhclient não está disponível. Consulte o README sobre NetworkManager.' >&2
  exit 1
fi
echo "A conexão de $interface será interrompida. Execute no terminal local."
read -r -p 'Digite RENOVAR para continuar: ' resposta
[[ "$resposta" == 'RENOVAR' ]] || exit 0
# Uma renovação pode mostrar só Request/Ack, sem um novo DORA completo.
dhclient -r "$interface"
dhclient -v "$interface"
