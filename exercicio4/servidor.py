# Participantes: [Jean Aquilla] 
from datetime import datetime
import logging
import threading
from comum import argumentos, enviar, executar, receber, servir_tcp

total = 0
trava = threading.Lock()


def atender(cliente, endereco):
    global total
    with cliente, cliente.makefile("rb") as arquivo:
        try:
            cliente.settimeout(10)
            pedido = receber(arquivo)
            if pedido != "HORA":
                enviar(cliente, "Erro: envie HORA")
                return
            # Reserva um número único para cada solicitação válida.
            with trava:
                total += 1
                numero = total
            logging.info("Recebida %s:%s contador=%d", *endereco, numero)
            hora = datetime.now().strftime("%H:%M:%S")
            enviar(cliente, hora)
            logging.info("Atendida %s:%s contador=%d hora=%s", *endereco, numero, hora)
            # A resposta é texto TCP; este exercício não usa NTP.
        except (OSError, ValueError) as erro:
            with trava:
                atual = total
            logging.info("Falha %s:%s contador=%d erro=%s", *endereco, atual, erro)


if __name__ == "__main__":
    executar(lambda: servir_tcp(argumentos("Servidor de hora", 7000), atender))
