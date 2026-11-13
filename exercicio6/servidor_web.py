# Participantes: [Jean Aquilla] 
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from comum import argumentos, executar


class Pagina(BaseHTTPRequestHandler):
    def do_GET(self):
        corpo = b"Conexao TCP observada.\n"
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(corpo)))
        self.send_header("Connection", "close")
        self.end_headers()
        self.wfile.write(corpo)
        self.close_connection = True
        # O fechamento permite localizar FIN/ACK após a resposta HTTP.


def main():
    args = argumentos("Servidor HTTP para telnet", 80)
    with ThreadingHTTPServer((args.host, args.porta), Pagina) as servidor:
        print(f"Servidor em {args.host}:{args.porta}", flush=True)
        servidor.serve_forever()


if __name__ == "__main__":
    executar(main)
