# Exercício 4 — Servidor de hora

Participantes: Jean Aquilla

Na raiz, com Python 3.10+ e sem dependências externas:

```bash
# Terminal 1
python3 -m exercicio4.servidor --host 127.0.0.1 --porta 7000
# Terminal 2; repita ou use os testes para chamadas concorrentes
python3 -m exercicio4.cliente --host 127.0.0.1 --porta 7000
```
