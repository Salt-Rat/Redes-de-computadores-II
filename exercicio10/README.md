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

Abra `http://127.0.0.1:8000/cliente.html` em três abas. Escolha nomes diferentes, mantenha `ws://127.0.0.1:8765` e clique em Conectar. Envie mensagens e confirme o recebimento nas outras abas. `sair` encerra uma conexão; fechar uma aba também não deve derrubar os demais participantes.

O primeiro frame de texto informa o nome; os seguintes são mensagens. Nomes têm entre 1 e 30 caracteres. Frames têm até 4096 bytes. Mensagens vazias são ignoradas e nomes duplicados são recusados. O servidor usa asyncio; cada conexão é uma tarefa, sem thread por usuário. As próprias mensagens aparecem localmente no navegador como `Você`, e o servidor só as retransmite aos outros clientes.

Capture em `lo` e filtre `tcp.port == 8765`. Observe o handshake TCP, o GET HTTP com Upgrade: websocket, a resposta 101 e os frames WebSocket. Use `websocket` depois do upgrade; se necessário, configure Decode As → HTTP para a porta. Frames enviados pelo navegador são mascarados, mas mascaramento não é criptografia. O exemplo usa `ws://`, sem TLS, e desativa compressão para facilitar a leitura. `wss://` exigiria configuração TLS adicional.

Salve `exercicio10/captura.pcapng`. A porta HTTP 8000 serve o HTML e é distinta da conexão WebSocket em 8765.
