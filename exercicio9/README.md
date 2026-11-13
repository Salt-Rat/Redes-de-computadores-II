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

O script exige confirmação `RENOVAR`, libera e pede uma concessão. Não execute dhclient junto de outro gerenciador na mesma interface. Caso use NetworkManager, prefira as configurações gráficas ou `nmcli connection show --active`, seguido de `nmcli connection down id 'NOME'` e `nmcli connection up id 'NOME'`, com o nome real da conexão. A disponibilidade de dhclient e os comandos variam entre distribuições.

Uma concessão existente pode produzir somente Request/ACK, mesmo após reconectar. Para obter DORA completo, faça uma nova aquisição em uma VM/rede de laboratório com configuração limpa e capture desde antes de conectar. Não apague concessões nem altere a rede principal sem necessidade. Não preencha Discover/Offer como observados se não aparecerem.

No Discover, o cliente ainda pode usar origem `0.0.0.0` e destino broadcast. O servidor usa UDP 67 e o cliente UDP 68. Em Offer/ACK, anote o endereço ofertado e opções de máscara, roteador, DNS e lease; opções ausentes devem ser registradas como ausentes. O DHCP Message Type está na opção 53. Filtros: `dhcp.option.dhcp == 1` (Discover), `== 2` (Offer), `== 3` (Request), `== 5` (ACK).

Salve `exercicio9/captura.pcapng` e `exercicio9/evidencia.png`, mostrando as quatro mensagens da mesma negociação.

## Observações da captura — preencher após executar

O cliente [MAC] iniciou a negociação na interface [nome], com Transaction ID [valor].  
Discover, Offer, Request e ACK ocorreram nos pacotes [números ou ausentes].  
O servidor [IP] atribuiu [IPv4], com máscara [valor] e gateway [valor].  
Foram informados DNS [valor] e lease [valor]; [registrar se foi renovação parcial].
