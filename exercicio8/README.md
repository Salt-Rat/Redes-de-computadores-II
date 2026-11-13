# Exercício 8 — ICMP e RTT

Participantes: Jean Aquilla

Requisitos: Linux, Wireshark e ping (`sudo apt install iputils-ping`). Identifique o IP de um computador da sua rede que responda a ping; o gateway aparece em `ip route` e também serve como alvo local se permitido.

Inicie a captura na interface de rede. Na raiz, substitua o endereço pelo alvo real:

```bash
bash exercicio8/ping_rede.sh 192.168.1.1
```
