# Exercício 2 — Echo UDP

Participantes: Jean Aquilla

Na raiz, com Python 3.10+ e sem dependências externas:

```bash
# Terminal 1
python -m exercicio2.servidor --host 127.0.0.1 --porta 6000
# Terminal 2
python -m exercicio2.cliente --host 127.0.0.1 --porta 6000
```

Digite texto e confira o eco. `sair` encerra. O tamanho é calculado em bytes UTF-8, com limite de 65.507. Sem resposta em três segundos, o cliente informa timeout; sistemas também podem retornar erro ICMP como conexão recusada. Não há retransmissão automática de aplicação.

Capture em `lo`, filtre `udp.port == 6000` e procure os datagramas de ida e volta. Não existe handshake TCP. O eco é resposta da aplicação, não ACK do UDP. Mensagens próximas do limite podem fragmentar; nesse caso, inclua também `ip.flags.mf == 1 || ip.frag_offset > 0` no filtro para ver os fragmentos. Salve `exercicio2/captura.pcapng`.
