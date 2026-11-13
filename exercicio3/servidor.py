# Participantes: [Jean Aquilla]
import logging
import threading
from comum import argumentos, enviar, executar, receber, servir_tcp

clientes = {}
trava_clientes = threading.Lock()


def transmitir(texto, origem):
    with trava_clientes:
        destinos = [(sock, dados[1]) for sock, dados in clientes.items() if sock != origem]
    for sock, trava_envio in destinos:
        try:
            # Serializa escritas de threads diferentes no mesmo cliente.
            with trava_envio:
                enviar(sock, texto)
        except OSError:
            try:
                sock.shutdown(2)
            except OSError:
                pass


def atender(cliente, endereco):
    nome = None
    with cliente, cliente.makefile("rb") as arquivo:
        try:
            cliente.settimeout(15)
            apelido = receber(arquivo)
            if not apelido or not apelido.strip() or len(apelido.strip()) > 30:
                enviar(cliente, "Erro: nome deve ter entre 1 e 30 caracteres")
                return
            apelido = apelido.strip()
            with trava_clientes:
                if any(dados[0] == apelido for dados in clientes.values()):
                    enviar(cliente, "Erro: nome já está em uso")
                    return
                enviar(cliente, "Conectado. Digite sair para encerrar.")
                clientes[cliente] = (apelido, threading.Lock())
                nome = apelido
            cliente.settimeout(None)
            transmitir(f"* {nome} entrou", cliente)
            while (texto := receber(arquivo)) is not None:
                if texto.strip().lower() == "sair":
                    break
                if texto.strip():
                    if len(f"{nome}: {texto.strip()}".encode("utf-8")) > 4096:
                        with trava_clientes:
                            trava_envio = clientes[cliente][1]
                        with trava_envio:
                            enviar(cliente, "Erro: mensagem com nome excede 4096 bytes")
                        continue
                    # Cada destinatário tem sua própria conexão TCP.
                    transmitir(f"{nome}: {texto.strip()}", cliente)
        except (OSError, ValueError) as erro:
            logging.info("Cliente %s:%s: %s", *endereco, erro)
        finally:
            if nome:
                with trava_clientes:
                    clientes.pop(cliente, None)
                transmitir(f"* {nome} saiu", cliente)


if __name__ == "__main__":
    executar(lambda: servir_tcp(argumentos("Chat TCP", 5001), atender))
