# Exercício 4 — Servidor de hora

Participantes: Jean Aquilla

Na raiz, com Python 3.10+ e sem dependências externas:

```bash
# Terminal 1
python -m exercicio4.servidor --host 127.0.0.1 --porta 7000
# Terminal 2; repita ou use os testes para chamadas concorrentes
python -m exercicio4.cliente --host 127.0.0.1 --porta 7000
```

O cliente envia `HORA` e recebe a hora local do servidor em `HH:MM:SS`. O contador é incrementado uma vez por conexão com pedido válido, antes do envio. Uma falha posterior de entrega não desfaz esse número. As linhas de solicitação e atendimento registram data/hora, cliente e contador. A ordem dos logs pode variar entre threads, mas os números reservados são únicos. Conexões sem pedido expiram em dez segundos.

No Wireshark, filtre `tcp.port == 7000`, identifique `HORA` e a resposta com Follow → TCP Stream. O protocolo é próprio e não é NTP. Salve `exercicio4/captura.pcapng`.
