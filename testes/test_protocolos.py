# Participantes: [Jean Aquilla] 
"""Testes reais em loopback; execute a partir da raiz do projeto."""
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
import importlib.util
from pathlib import Path
import re
import socket
import subprocess
import sys
import time
import unittest
from urllib.request import urlopen

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from comum import enviar, receber

RAIZ = Path(__file__).resolve().parents[1]
TEM_WS = importlib.util.find_spec("websockets") is not None


def porta_livre(udp=False):
    with socket.socket(type=socket.SOCK_DGRAM if udp else socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


@contextmanager
def servidor(modulo, udp=False):
    porta = porta_livre(udp)
    processo = subprocess.Popen(
        [sys.executable, "-m", modulo, "--host", "127.0.0.1", "--porta", str(porta)],
        cwd=RAIZ, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True,
        encoding="utf-8", errors="replace")
    try:
        for _ in range(100):
            if processo.poll() is not None:
                raise RuntimeError(processo.stderr.read())
            try:
                with socket.socket(type=socket.SOCK_DGRAM if udp else socket.SOCK_STREAM) as sock:
                    sock.settimeout(0.1)
                    sock.connect(("127.0.0.1", porta))
                    if udp:
                        sock.send(b"pronto")
                        if sock.recv(100) != b"pronto":
                            continue
                break
            except OSError:
                time.sleep(0.05)
        else:
            raise RuntimeError("Servidor não ficou pronto.")
        yield porta, processo
    finally:
        processo.terminate()
        try:
            processo.wait(timeout=5)
        except subprocess.TimeoutExpired:
            processo.kill()
            processo.wait()
        processo.stderr.close()


@contextmanager
def conexao(porta):
    with socket.create_connection(("127.0.0.1", porta), timeout=3) as sock:
        with sock.makefile("rb") as arquivo:
            yield sock, arquivo


class Protocolos(unittest.TestCase):
    def test_tcp_fluxo_vazio_fragmentado_e_concorrente(self):
        with servidor("exercicio1.servidor") as (porta, _):
            with conexao(porta) as (sock, arquivo):
                sock.sendall(b"\num\ndois\nparte")
                self.assertIn("vazia", receber(arquivo))
                self.assertEqual(receber(arquivo), "Mensagem recebida")
                self.assertEqual(receber(arquivo), "Mensagem recebida")
                sock.sendall(b"final\n")
                self.assertEqual(receber(arquivo), "Mensagem recebida")

            def tarefa(_):
                with conexao(porta) as (sock, arquivo):
                    enviar(sock, "Olá")
                    return receber(arquivo)
            with ThreadPoolExecutor(max_workers=6) as pool:
                self.assertEqual(list(pool.map(tarefa, range(12))), ["Mensagem recebida"] * 12)

    def test_tcp_recusa_linha_longa_e_continua(self):
        with servidor("exercicio1.servidor") as (porta, _):
            with conexao(porta) as (sock, arquivo):
                sock.sendall(b"x" * 5000 + b"\n")
                try:
                    self.assertEqual(arquivo.read(1), b"")
                except ConnectionResetError:
                    pass
            with conexao(porta) as (sock, arquivo):
                enviar(sock, "Ainda funciona")
                self.assertEqual(receber(arquivo), "Mensagem recebida")

    def test_udp_preserva_bytes(self):
        with servidor("exercicio2.servidor", udp=True) as (porta, _):
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                sock.settimeout(3)
                for dados in ["Olá rede".encode(), bytes(range(256)), b"x" * 1200]:
                    sock.sendto(dados, ("127.0.0.1", porta))
                    resposta, _ = sock.recvfrom(65507)
                    self.assertEqual(resposta, dados)

    def test_clientes_interativos_tcp_e_hora(self):
        with servidor("exercicio1.servidor") as (porta, _):
            resultado = subprocess.run(
                [sys.executable, "-m", "exercicio1.cliente", "--porta", str(porta)],
                cwd=RAIZ, input="\nTeste\nsair\n", capture_output=True,
                text=True, timeout=10)
            self.assertEqual(resultado.returncode, 0, resultado.stderr)
            self.assertIn("Digite uma mensagem", resultado.stdout)
            self.assertIn("Mensagem recebida", resultado.stdout)
        with servidor("exercicio4.servidor") as (porta, _):
            resultado = subprocess.run(
                [sys.executable, "-m", "exercicio4.cliente", "--porta", str(porta)],
                cwd=RAIZ, capture_output=True, text=True, timeout=10)
            self.assertEqual(resultado.returncode, 0, resultado.stderr)
            self.assertRegex(resultado.stdout, r"Hora do servidor: \d{2}:\d{2}:\d{2}")

    def test_cliente_udp_tamanho_timeout_e_eco(self):
        with servidor("exercicio2.servidor", udp=True) as (porta, _):
            resultado = subprocess.run(
                [sys.executable, "-m", "exercicio2.cliente", "--porta", str(porta)],
                cwd=RAIZ, input="x" * 65508 + "\nTeste\nsair\n", capture_output=True,
                text=True, timeout=10)
            self.assertEqual(resultado.returncode, 0, resultado.stderr)
            self.assertIn("65507 bytes", resultado.stdout)
            self.assertIn("Eco: Teste", resultado.stdout)
        # Porta ocupada, sem responder: garante timeout em vez de ICMP de porta fechada.
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as silencioso:
            silencioso.bind(("127.0.0.1", 0))
            resultado = subprocess.run(
                [sys.executable, "-m", "exercicio2.cliente", "--porta",
                 str(silencioso.getsockname()[1])], cwd=RAIZ,
                input="Teste\nsair\n", capture_output=True, text=True, timeout=10)
            self.assertEqual(resultado.returncode, 0, resultado.stderr)
            self.assertIn("Sem resposta em 3 segundos", resultado.stdout)

    def test_chat_tres_usuarios_entrada_broadcast_saida(self):
        with servidor("exercicio3.servidor") as (porta, _):
            with conexao(porta) as (a, fa), conexao(porta) as (b, fb), conexao(porta) as (c, fc):
                enviar(a, "Ana")
                self.assertIn("Conectado", receber(fa))
                enviar(b, "Bia")
                self.assertIn("Conectado", receber(fb))
                self.assertEqual(receber(fa), "* Bia entrou")
                enviar(c, "Caio")
                self.assertIn("Conectado", receber(fc))
                self.assertEqual(receber(fa), "* Caio entrou")
                self.assertEqual(receber(fb), "* Caio entrou")
                enviar(a, "Oi")
                self.assertEqual(receber(fb), "Ana: Oi")
                self.assertEqual(receber(fc), "Ana: Oi")
                enviar(c, "sair")
                self.assertEqual(receber(fa), "* Caio saiu")
                self.assertEqual(receber(fb), "* Caio saiu")
                enviar(b, "Continuamos")
                self.assertEqual(receber(fa), "Bia: Continuamos")

    def test_chat_nome_duplicado_e_mensagem_longa(self):
        with servidor("exercicio3.servidor") as (porta, _):
            with conexao(porta) as (a, fa), conexao(porta) as (b, fb):
                enviar(a, "Ana")
                self.assertIn("Conectado", receber(fa))
                enviar(b, "Ana")
                self.assertIn("Erro", receber(fb))
                enviar(a, "x" * 4096)
                self.assertIn("excede", receber(fa))

    def test_hora_concorrencia_e_contador(self):
        with servidor("exercicio4.servidor") as (porta, processo):
            with conexao(porta) as (sock, arquivo):
                enviar(sock, "INVALIDO")
                self.assertIn("Erro", receber(arquivo))

            def tarefa(_):
                with conexao(porta) as (sock, arquivo):
                    enviar(sock, "HORA")
                    return receber(arquivo)
            with ThreadPoolExecutor(max_workers=6) as pool:
                respostas = list(pool.map(tarefa, range(12)))
            for resposta in respostas:
                self.assertRegex(resposta, r"^\d{2}:\d{2}:\d{2}$")
            # Todos os logs são pequenos o suficiente para caber no pipe.
            time.sleep(0.1)
            processo.terminate()
            processo.wait(timeout=5)
            logs = processo.stderr.read()
            numeros = [int(x) for x in re.findall(r"Recebida .*contador=(\d+)", logs)]
            self.assertEqual(sorted(numeros), list(range(1, 13)))

    def test_http_campos(self):
        for modulo in ("exercicio5.servidor_http", "exercicio6.servidor_web"):
            with self.subTest(modulo=modulo), servidor(modulo) as (porta, _):
                with urlopen(f"http://127.0.0.1:{porta}/teste", timeout=3) as resposta:
                    self.assertEqual(resposta.status, 200)
                    self.assertIn("text/", resposta.headers["Content-Type"])
                    self.assertTrue(resposta.headers["Server"])
                    self.assertTrue(resposta.read())

    @unittest.skipUnless(TEM_WS, "Instale requirements.txt para testar WebSocket")
    def test_websocket_broadcast_e_desconexao(self):
        from websockets.sync.client import connect
        with servidor("exercicio10.servidor") as (porta, _):
            url = f"ws://127.0.0.1:{porta}"
            with connect(url, proxy=None) as a, connect(url, proxy=None) as b:
                a.send("Ana")
                self.assertIn("Conectado", a.recv(timeout=3))
                b.send("Bia")
                self.assertIn("Conectado", b.recv(timeout=3))
                self.assertEqual(a.recv(timeout=3), "* Bia entrou")
                a.send("Oi")
                self.assertEqual(b.recv(timeout=3), "Ana: Oi")
                b.close()
                self.assertEqual(a.recv(timeout=3), "* Bia saiu")
                with connect(url, proxy=None) as c:
                    c.send("Caio")
                    self.assertIn("Conectado", c.recv(timeout=3))
                    self.assertEqual(a.recv(timeout=3), "* Caio entrou")
                    c.send("Ainda funciona")
                    self.assertEqual(a.recv(timeout=3), "Caio: Ainda funciona")

    def test_cliente_conexao_recusada(self):
        resultado = subprocess.run(
            [sys.executable, "-m", "exercicio1.cliente", "--porta", str(porta_livre())],
            cwd=RAIZ, capture_output=True, text=True, timeout=10)
        self.assertNotEqual(resultado.returncode, 0)
        self.assertIn("Erro:", resultado.stderr)
        self.assertNotIn("Traceback", resultado.stderr)


if __name__ == "__main__":
    unittest.main()
