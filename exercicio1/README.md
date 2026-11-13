# Exercício 1 — Confirmação TCP

Participantes: Jean Aquilla

Na raiz do projeto, com Python 3.10+ e sem dependências externas, abra dois terminais:

```bash
# Terminal 1
python3 -m exercicio1.servidor --host 127.0.0.1 --porta 5000
# Terminal 2; repita em outros terminais para testar concorrência
python3 -m exercicio1.cliente --host 127.0.0.1 --porta 5000
```

Digite várias mensagens. Cada uma recebe `Mensagem recebida`. Entradas vazias são rejeitadas e `sair` fecha o cliente. O servidor registra data/hora, IP, porta e mensagem. Mensagens têm até 4096 bytes UTF-8 e são separadas por `\n`.

No Wireshark, capture em `lo`, filtre `tcp.port == 5000` e use Follow → TCP Stream. Observe handshake, mensagem, confirmação e fechamento. Não espere um pacote por mensagem: TCP pode segmentar ou juntar dados. Salve `exercicio1/captura.pcapng`.
