# Exercício 9 — DHCP

Participantes: Jean Aquilla

Requisitos: Linux com cliente DHCPv4, rede que forneça IPv4 por DHCP e Wireshark. Este exercício deve ser feito no terminal local: a liberação da concessão pode interromper o acesso à rede. Não é preciso executar o auxiliar para entender o código.

1. Descubra a interface com `ip -br link` e inicie a captura nela, sem filtro de captura restritivo.
2. Desconecte e reconecte a rede pelas configurações do Linux.
3. Filtre `dhcp` (em versões antigas, `bootp`) ou `udp.port == 67 || udp.port == 68`.
4. Procure Discover, Offer, Request e ACK. Correlacione Transaction ID e MAC do cliente; não misture negociações de máquinas diferentes.

Se a distribuição usa dhclient e ele é o cliente responsável pela interface, o auxiliar executa os comandos indicados no trabalho:

```bash
# Na raiz; substitua enp0s3 pelo nome real.
sudo bash exercicio9/renovar_dhcp.sh enp0s3
```
