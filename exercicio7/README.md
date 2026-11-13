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
