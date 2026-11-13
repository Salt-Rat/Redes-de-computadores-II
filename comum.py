# Participantes: [Jean Aquilla] 
"""Rotinas compartilhadas pelos exercícios de sockets."""

import argparse
import logging
import socket
import threading

MAX_TEXTO = 4096


def porta(valor):
    numero = int(valor)
    if not 1 <= numero <= 65535:
        raise argparse.ArgumentTypeError("A porta deve estar entre 1 e 65535.")
    return numero


def argumentos(descricao, padrao):
    parser = argparse.ArgumentParser(description=descricao)
    parser.add_argument("--host", default="127.0.0.1", help="IPv4 ou nome do host")
    parser.add_argument("--porta", type=porta, default=padrao)
    return parser.parse_args()


def configurar_log():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S")


def enviar(sock, texto):
    # A quebra de linha delimita mensagens no fluxo TCP.
    dados = texto.encode("utf-8")
    if b"\n" in dados or b"\r" in dados or len(dados) > MAX_TEXTO:
        raise ValueError("Use uma linha de até 4096 bytes UTF-8.")
    sock.sendall(dados + b"\n")


def receber(arquivo):
    linha = arquivo.readline(MAX_TEXTO + 2)
    if not linha:
        return None
    if not linha.endswith(b"\n") or len(linha) > MAX_TEXTO + 1:
        raise ValueError("Mensagem longa ou sem delimitador.")
    return linha[:-1].decode("utf-8").removesuffix("\r")


def servir_tcp(args, atender):
    configurar_log()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        servidor.bind((args.host, args.porta))
        servidor.listen()
        logging.info("Escutando em %s:%s", args.host, args.porta)
        try:
            while True:
                cliente, endereco = servidor.accept()
                threading.Thread(target=atender, args=(cliente, endereco), daemon=True).start()
        except KeyboardInterrupt:
            logging.info("Servidor encerrado.")


def executar(funcao):
    try:
        funcao()
    except (KeyboardInterrupt, EOFError):
        print("\nEncerrado.")
    except (OSError, ValueError) as erro:
        raise SystemExit(f"Erro: {erro}") from None
