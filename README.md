# Trabalho 2 de Redes de Computadores 2

Professor: Alessandro Vivas Andrade  
Participante 1: Jean Aquila Rodrigues Corrêa 
 
Turma:  Redes de Computadores II  Data: 13/11/26

## Objetivo

Implementar comunicação TCP, UDP e WebSocket e observar HTTP, TCP, DNS, ICMP e DHCP no Wireshark. Os exercícios estão separados por pasta. Os comentários do código resumem decisões de implementação!

## Preparação no Linux

 Python 3.10 ou superior.(Ubuntu/Debian)

```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip wireshark dnsutils iputils-ping telnet
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Execute todos os comandos a partir da raiz do projeto, onde está `comum.py`. Os programas são chamados com `python -m exercicioN.programa`; executar o arquivo pelo caminho pode impedir a importação de `comum`. A única dependência Python externa é `websockets==15.0.1`, usada no exercício 10. Use `--help` para consultar host e porta. Os scripts `.sh` são executados com `bash`, sem precisar de `chmod`.

O host padrão é `127.0.0.1`, para testes na própria máquina. Para computadores diferentes, inicie o servidor com `--host 0.0.0.0` e configure o cliente com o IPv4 real do servidor. `0.0.0.0` é endereço de escuta, não destino de conexão. Libere a porta no firewall quando necessário.

## Organização e execução

| Pasta | Conteúdo | Porta padrão |
| --- | --- | --- |
| exercicio1 | Cliente e servidor TCP com confirmação | TCP 5000 |
| exercicio2 | Cliente e servidor UDP echo | UDP 6000 |
| exercicio3 | Chat TCP com threads | TCP 5001 |
| exercicio4 | Consulta de hora e contador com Lock | TCP 7000 |
| exercicio5 | Servidor HTTP e análise de cabeçalhos | TCP 8080 |
| exercicio6 | Servidor HTTP para conexão com telnet | TCP 80 |
| exercicio7 | Consultas DNS e roteiro de análise | UDP/TCP 53 |
| exercicio8 | Ping IPv4 e análise de RTT | ICMP, sem portas |
| exercicio9 | Roteiro e auxiliar de renovação DHCP | UDP 67/68 |
| exercicio10 | Servidor Python e cliente HTML WebSocket | TCP 8765 |

Cada pasta contém um README com os comandos completos. Os exercícios 1 a 4 precisam de terminais separados para servidor e clientes. `sair` encerra os clientes interativos e `Ctrl+C` encerra os servidores. No chat TCP, se o servidor cair enquanto o terminal aguarda entrada, pressione Enter para liberar o prompt.

## Parte escrita

O TCP oferece um fluxo de bytes confiável e ordenado. Os exercícios 1, 3 e 4 delimitam cada mensagem com uma quebra de linha. O servidor cria uma thread por conexão, permitindo atender vários clientes. O chat protege a lista de usuários e os envios concorrentes com locks. O servidor de hora protege o contador para que dois clientes não recebam o mesmo número de atendimento.

O UDP trabalha com datagramas independentes. O serviço echo devolve exatamente os bytes recebidos e o cliente aguarda por até três segundos. O limite validado é de 65.507 bytes de payload sobre IPv4. Esse valor é teórico: mensagens grandes podem sofrer fragmentação ou falhar por limitações da rede.

O WebSocket inicia com uma negociação HTTP e mantém uma conexão TCP para trocar mensagens em ambos os sentidos. O servidor usa tarefas assíncronas, identifica os usuários pelo nome e distribui as mensagens aos outros participantes. O cliente HTML usa a API WebSocket do navegador.

Nas capturas, os dados de aplicação devem ser relacionados aos protocolos de transporte e rede. HTTP permite identificar método, URL e cabeçalhos; TCP mostra abertura e encerramento; DNS mostra consultas e respostas; ICMP permite medir RTT; DHCP mostra a atribuição de configuração IPv4.

## Verificação e entrega

```bash
python -m unittest discover -s testes -v
```


## Referências técnicas

- [Sockets do Python](https://docs.python.org/3.10/library/socket.html)
- [Threads do Python](https://docs.python.org/3.10/library/threading.html)
- [Servidor assíncrono websockets 15.0.1](https://websockets.readthedocs.io/en/15.0.1/reference/asyncio/server.html)
- [Manual do Wireshark](https://www.wireshark.org/docs/wsug_html/)
- [Filtros ICMP](https://www.wireshark.org/docs/dfref/i/icmp.html)
- [Filtros DHCP](https://www.wireshark.org/docs/dfref/d/dhcp.html)
# Redes-de-computadores-II
