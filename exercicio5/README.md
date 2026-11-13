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

O exemplo local responde 200 e inclui os cabeçalhos pedidos. O navegador pode solicitar `/favicon.ico` em outra conexão. A URL completa combina esquema `http`, Host e caminho; o campo de requisição normalmente traz somente `/teste`. Em sites HTTPS, os cabeçalhos ficam dentro de TLS e o filtro HTTP pode ficar vazio. Se usar outro servidor, um cabeçalho Server ausente deve ser registrado como ausente.

## Observações da captura — preencher após executar

Foi acessada a URL [URL], com método [método], no pacote [número].  
A resposta do pacote [número] apresentou status [código].  
O Content-Type encontrado foi [valor] e o Server foi [valor ou ausente].  
Os cabeçalhos foram observados em [interface], no fluxo TCP [número].
