#!/usr/bin/env bash
# Participantes: [Jean Aquilla] 
set -euo pipefail
dominio="${1:-example.com}"
servidor="${2:-}"
if ! command -v dig >/dev/null; then
  echo 'Instale dig: sudo apt install dnsutils' >&2
  exit 1
fi
destino=()
if [[ -n "$servidor" ]]; then destino=("@$servidor"); fi
# Consultas explícitas evitam depender do cache do navegador ou de DoH.
dig "${destino[@]}" -q "$dominio" -t A +time=3 +tries=1
dig "${destino[@]}" -q "$dominio" -t AAAA +time=3 +tries=1
