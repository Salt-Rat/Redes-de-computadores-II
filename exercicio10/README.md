# Exercício 10 — Chat WebSocket

Participantes: Jean Aquilla

Requisitos: Python 3.10+, `websockets==15.0.1` e navegador com WebSocket. Na raiz:

```bash
python -m pip install -r requirements.txt
# Terminal 1
python -m exercicio10.servidor --host 127.0.0.1 --porta 8765
# Terminal 2: disponibiliza o cliente HTML
python -m http.server 8000 --bind 127.0.0.1 --directory exercicio10
```
