# Participantes: [Jean Aquilla]
import socket
from comum import argumentos, executar

MAX_UDP = 65507


def main():
    args = argumentos("Cliente UDP echo", 6000)
    while True:
        texto = input("Mensagem (sair para terminar): ")
        if texto.strip().lower() == "sair":
            break
        dados = texto.encode("utf-8")
        if not dados or len(dados) > MAX_UDP:
            print("Use de 1 a 65507 bytes UTF-8.")
            continue
        try:
            # Um socket por tentativa evita reaproveitar um eco atrasado.
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                sock.settimeout(3)
                sock.connect((args.host, args.porta))
                sock.send(dados)
                resposta = sock.recv(MAX_UDP)
                print("Eco:", resposta.decode("utf-8"))
        except TimeoutError:
            print("Sem resposta em 3 segundos.")
        except OSError as erro:
            print(f"Falha UDP: {erro}")


if __name__ == "__main__":
    executar(main)
