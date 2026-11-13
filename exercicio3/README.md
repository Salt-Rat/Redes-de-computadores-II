# Exercício 3 — Chat TCP

Participantes: Jean Aquilla

Na raiz, com Python 3.10+ e sem dependências externas:

```bash
# Terminal 1
python3 -m exercicio3.servidor --host 127.0.0.1 --porta 5001
# Terminais 2, 3 e 4
python3 -m exercicio3.cliente --host 127.0.0.1 --porta 5001
```

Escolha nomes diferentes de 1 a 30 caracteres. As mensagens são entregues aos outros usuários com o nome do remetente. A entrada e a saída são notificadas. Digite `sair` para desconectar um usuário e confirme que os demais continuam conversando. A leitura usa uma thread separada; mensagens podem aparecer enquanto o prompt de digitação está visível.

O servidor protege o cadastro com um Lock e cada socket com um Lock de envio. O nome deve chegar em até 15 segundos. O limite de 4096 bytes vale para cada linha no protocolo; o prefixo com o nome também ocupa bytes na retransmissão, portanto prefira mensagens curtas.

Capture em `lo`, filtre `tcp.port == 5001` e use `tcp.stream eq N` para examinar cada conexão. O broadcast é feito pela aplicação com envios TCP separados: não é broadcast Ethernet/IP. Salve `exercicio3/captura.pcapng`.
