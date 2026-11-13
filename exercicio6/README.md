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
