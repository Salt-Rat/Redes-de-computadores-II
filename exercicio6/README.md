# Exercício 6 — Abertura e encerramento TCP

Participantes: Jean Aquilla
Requisitos: Python 3.10+, telnet e Wireshark. Na raiz, no Linux:

```bash
# Porta 80 pode exigir privilégio; usa explicitamente o Python do ambiente virtual.
sudo .venv/bin/python -m exercicio6.servidor_web --host 127.0.0.1 --porta 80
# Em outro terminal, após iniciar a captura em lo:
telnet 127.0.0.1 80
```

Digite estas linhas e pressione Enter novamente após a última, formando uma linha vazia:

```http
GET / HTTP/1.0
Host: localhost
Connection: close

```

Pare a captura após o encerramento. Filtre `tcp.port == 80`, selecione a conexão e use `tcp.stream eq N`, trocando N pelo índice. Localize SYN, SYN/ACK, ACK e FIN/ACK. Filtros auxiliares: `tcp.flags.syn == 1`, `tcp.flags.fin == 1`, `tcp.flags.reset == 1`. O ACK isolado também aparece em outros momentos: confirme sequência e sentido. FIN e ACK podem ser combinados, por isso o fechamento não tem sempre quatro pacotes separados.

Se a porta 80 estiver ocupada, use outro host com HTTP na porta 80 ou encerre somente o serviço que você administra. Para estudo, pode usar `--porta 8081` sem sudo e `telnet 127.0.0.1 8081`, mas o enunciado pede porta 80: registre a diferença e confirme sua aceitação com o professor.

Salve `exercicio6/captura.pcapng` e `exercicio6/evidencia.png` destacando abertura e fechamento (use duas imagens se necessário).

## Observações da captura — preencher após executar

A conexão ocorreu de [IP:porta cliente] para [IP:porta servidor], no fluxo [N].  
Os pacotes [números] mostraram SYN, SYN/ACK e ACK, respectivamente.  
O encerramento apresentou [FIN/ACK ou RST] nos pacotes [números].  
A sequência observada indica [interpretação do encerramento].
