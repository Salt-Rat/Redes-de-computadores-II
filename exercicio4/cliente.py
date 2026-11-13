# Participantes: [Jean Aquilla]
import socket
from comum import argumentos, enviar, executar, receber


def main():
    args = argumentos("Cliente de hora", 7000)
    with socket.create_connection((args.host, args.porta), timeout=5) as sock:
        with sock.makefile("rb") as arquivo:
            enviar(sock, "HORA")
            resposta = receber(arquivo)
            if resposta is None:
                raise ValueError("Servidor fechou sem enviar a hora.")
            print("Hora do servidor:", resposta)


if __name__ == "__main__":
    executar(main)
