# Participantes: [Jean Aquilla] 
import logging
import socket
from comum import argumentos, configurar_log, executar

MAX_UDP = 65507


def main():
    args = argumentos("Servidor UDP echo", 6000)
    configurar_log()
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind((args.host, args.porta))
        logging.info("UDP em %s:%s", args.host, args.porta)
        while True:
            dados, endereco = sock.recvfrom(MAX_UDP)
            logging.info("%s:%s (%d bytes): %s", *endereco, len(dados),
                         dados.decode("utf-8", errors="replace"))
            try:
                # Eco preserva os bytes; não há handshake nem ACK de transporte.
                sock.sendto(dados, endereco)
            except OSError as erro:
                logging.warning("Falha no eco para %s: %s", endereco, erro)


if __name__ == "__main__":
    executar(main)
