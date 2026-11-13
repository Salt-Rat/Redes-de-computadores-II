# Participantes: [Jean Aquilla]
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from comum import argumentos, executar


class Pagina(BaseHTTPRequestHandler):
    server_version = "LaboratorioRedes/1.0"
    sys_version = ""

    def do_GET(self):
        corpo = b"<h1>Laboratorio de HTTP</h1><p>Requisicao recebida.</p>\n"
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(corpo)))
        self.end_headers()
        # HTTP simples permite ler método, caminho, status e cabeçalhos.
        self.wfile.write(corpo)


def main():
    args = argumentos("Página HTTP para captura", 8080)
    with ThreadingHTTPServer((args.host, args.porta), Pagina) as servidor:
        print(f"Abra http://{args.host}:{args.porta}/teste", flush=True)
        servidor.serve_forever()


if __name__ == "__main__":
    executar(main)
