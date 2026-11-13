# Exercício 5 — HTTP

Participantes: Jean Aquilla

Requisitos: Python 3.10+, navegador e Wireshark. Na raiz:

```bash
python -m exercicio5.servidor_http --host 127.0.0.1 --porta 8080
```

1. Inicie a captura em `lo`.
2. Abra `http://127.0.0.1:8080/teste` no navegador, usando HTTP explicitamente.
3. Pare a captura e aplique `http && tcp.port == 8080`. Se aparecer apenas TCP, use Analyze → Decode As → HTTP para a porta 8080.
4. Selecione o GET e a resposta. Expanda Hypertext Transfer Protocol. Identifique método, Host, URI, status, Content-Type e Server.
5. Salve `exercicio5/captura.pcapng` e uma imagem `exercicio5/evidencia.png` com os campos relevantes visíveis.
