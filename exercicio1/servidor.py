# Participantes: [Jean Aquilla]
import logging
from comum import argumentos, enviar, executar, receber, servir_tcp


def atender(cliente, endereco):
    with cliente, cliente.makefile("rb") as arquivo:
        try:
            while (mensagem := receber(arquivo)) is not None:
                if not mensagem.strip():
                    enviar(cliente, "Erro: mensagem vazia")
                    continue
                logging.info("%s:%s - %s", *endereco, mensagem)
                # No Wireshark, o texto fica visível em Follow TCP Stream.
                enviar(cliente, "Mensagem recebida")
        except (OSError, ValueError) as erro:
            logging.info("Cliente %s:%s desconectado: %s", *endereco, erro)


if __name__ == "__main__":
    executar(lambda: servir_tcp(argumentos("Servidor TCP", 5000), atender))
