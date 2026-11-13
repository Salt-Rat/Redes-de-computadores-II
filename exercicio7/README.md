# Exercício 7 — DNS

Participantes: Jean Aquilla

Requisitos: navegador, Wireshark e `dig` (`sudo apt install dnsutils` no Ubuntu/Debian).

1. Inicie a captura na interface de rede ativa; se necessário, inclua `lo` para o resolvedor local.
2. Acesse `http://example.com` no navegador e filtre `dns`. O tráfego da página pode ser redirecionado; o foco aqui é DNS.
3. Se o cache ou DNS sobre HTTPS impedir a visualização, use uma consulta explícita como complemento, a partir da raiz:

```bash
bash exercicio7/consultar_dns.sh example.com
# Para consultar um servidor específico permitido na sua rede:
bash exercicio7/consultar_dns.sh example.com 1.1.1.1
```

As consultas A e AAAA são separadas. Anote Transaction ID, nome e tipo em Queries, IP de destino e registros em Answers. A corresponde a IPv4, AAAA a IPv6 e CNAME a um apelido. Um CNAME só deve ser registrado se realmente aparecer. Resposta vazia ou negativa também é um resultado: registre o código e o conteúdo recebido. DNS pode usar TCP, além de UDP.

O campo SERVER do dig pode indicar `127.0.0.53`, um resolvedor local. Para saber o DNS externo, examine a interface física e `resolvectl status`, quando disponível. Não conclua que todo navegador usa DNS na porta 53: DoH fica dentro de HTTPS. Se só o dig gerou pacotes visíveis, registre essa diferença.

Salve `exercicio7/captura.pcapng` e `exercicio7/evidencia.png` com consulta e resposta.

## Observações da captura — preencher após executar

Foi consultado [domínio] com tipo [A/AAAA/outro], no pacote [número].  
O servidor DNS observado foi [IP], na interface [nome].  
A resposta [número] retornou [registros ou resposta negativa].  
O tráfego foi gerado por [navegador/dig], com Transaction ID [valor].
