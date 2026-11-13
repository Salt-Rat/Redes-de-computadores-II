# Participantes: [Jean Aquilla] 
import socket
from comum import argumentos, enviar, executar, receber


def main():
    args = argumentos("Cliente TCP", 5000)
    with socket.create_connection((args.host, args.porta), timeout=5) as sock:
        sock.settimeout(None)
        with sock.makefile("rb") as arquivo:
            while True:
                texto = input("Mensagem (sair para terminar): ")
                if texto.strip().lower() == "sair":
                    break
                if not texto.strip():
                    print("Digite uma mensagem.")
                    continue
                try:
                    enviar(sock, texto)
                except ValueError as erro:
                    print(erro)
                    continue
                resposta = receber(arquivo)
                if resposta is None:
                    print("Servidor encerrou a conexão.")
                    break
                print(resposta)
        # O fechamento normal produz FIN/ACK no TCP.


if __name__ == "__main__":
    executar(main)
