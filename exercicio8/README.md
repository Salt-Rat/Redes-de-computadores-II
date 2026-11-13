# Exercício 8 — ICMP e RTT

Participantes: Jean Aquilla

Requisitos: Linux, Wireshark e ping (`sudo apt install iputils-ping`). Identifique o IP de um computador da sua rede que responda a ping; o gateway aparece em `ip route` e também serve como alvo local se permitido.

Inicie a captura na interface de rede. Na raiz, substitua o endereço pelo alvo real:

```bash
bash exercicio8/ping_rede.sh 192.168.1.1
```

Pare a captura e filtre `icmp`. Echo Request tem tipo 8 e Echo Reply tem tipo 0 em IPv4. Relacione cada par por origem/destino, Identifier e Sequence Number. Na resposta, procure `icmp.resptime`, mostrado em milissegundos quando o Wireshark consegue associar o par. Alternativamente, subtraia os horários dos quadros: `RTT_ms = (tempo_resposta - tempo_pedido) * 1000`.

Não use o intervalo entre respostas consecutivas como RTT. A coluna time do ping já mostra o RTT medido pelo programa e pode diferir um pouco da captura. Pedido sem resposta é perda ou ausência de resposta observada; não atribua RTT zero. Salve `exercicio8/captura.pcapng` e `exercicio8/evidencia.png`.

| Sequência | Quadro pedido | Quadro resposta | RTT em ms |
| --- | --- | --- | --- |
| 1 | preencher | preencher | preencher |
| 2 | preencher | preencher | preencher |
| 3 | preencher | preencher | preencher |
| 4 | preencher | preencher | preencher |

## Observações da captura — preencher após executar

O destino testado foi [IP], pela interface [nome].  
Foram identificados [quantidade] pedidos e [quantidade] respostas.  
Os RTTs por sequência foram [valores em ms ou sem resposta].  
A associação utilizou Identifier [valor] e Sequence Number [valores].
