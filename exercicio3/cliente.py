# Participantes: [Jean Aquilla]
import socket
import threading
from comum import argumentos, enviar, executar, receber


def ler(arquivo, terminou):
    try:
        while (texto := receber(arquivo)) is not None:
            print(f"\n{texto}", flush=True)
    except (OSError, ValueError) as erro:
        print(f"\nRecepção encerrada: {erro}")
    finally:
        terminou.set()
        print("\nConexão encerrada. Pressione Enter se necessário.", flush=True)


def main():
    args = argumentos("Cliente do chat TCP", 5001)
    nome = input("Nome (1 a 30 caracteres): ").strip()
    if not 1 <= len(nome) <= 30:
        raise ValueError("Nome inválido.")
    with socket.create_connection((args.host, args.porta), timeout=5) as sock:
        sock.settimeout(None)
        with sock.makefile("rb") as arquivo:
            enviar(sock, nome)
            resposta = receber(arquivo)
            if resposta is None or resposta.startswith("Erro:"):
                print(resposta or "Servidor desconectou.")
                return
            print(resposta)
            terminou = threading.Event()
            thread = threading.Thread(target=ler, args=(arquivo, terminou), daemon=True)
            thread.start()
            try:
                while not terminou.is_set():
                    texto = input("> ")
                    if terminou.is_set():
                        break
                    if not texto.strip():
                        continue
                    try:
                        enviar(sock, texto)
                    except ValueError as erro:
                        print(erro)
                        continue
                    if texto.strip().lower() == "sair":
                        break
            finally:
                try:
                    sock.shutdown(socket.SHUT_RDWR)
                except OSError:
                    pass
                thread.join(timeout=2)


if __name__ == "__main__":
    executar(main)
