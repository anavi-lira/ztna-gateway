from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.request
from urllib.parse import urlparse, parse_qs

GATEWAY_HOST = "127.0.0.1"
GATEWAY_PORT = 9000
ALVO_REAL = "http://127.0.0.1:8080"


class ZTNAGateway(BaseHTTPRequestHandler):
    def verificar_postura(self):
        # 1. Verifica token via header
        token = self.headers.get('X-ZTNA-Token')

        # 2. Verifica token via URL query
        query = urlparse(self.path).query
        params = parse_qs(query)
        token_url = params.get("token", [None])[0]

        # 3. Verifica cookie
        cookie = self.headers.get('Cookie')
        cookie_valido = cookie and "ztna=senha_forte" in cookie

        if token == "senha_forte" or token_url == "senha_forte" or cookie_valido:
            return True
        return False

    def do_GET(self):
        print(f"--- Pedido recebido de: {self.client_address} ---")

        acesso_permitido = self.verificar_postura()

        if acesso_permitido:
            print(" Acesso PERMITIDO!")
            try:
                resposta_real = urllib.request.urlopen(ALVO_REAL)
                conteudo = resposta_real.read()

                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                # envia cookie ao navegador (ou ao cliente python)
                self.send_header("Set-Cookie", "ztna=senha_forte; Path=/")
                self.end_headers()
                self.wfile.write(conteudo)
            except Exception as e:
                self.send_error(500, f"Erro ao contactar servidor secreto: {e}")
        else:
            print("Acesso BLOQUEADO")
            self.send_response(403)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            msg_erro = """
            <html>
            <body style="background-color: #ffe0e0; color: red;">
            <h1>ACESSO NEGADO (ZERO TRUST)</h1>
            <p>O teu dispositivo não foi verificado ou não tens autorização.</p>
            <p>Tenta aceder com ?token=senha_forte ou via cliente Python.</p>
            </body>
            </html>
            """
            self.wfile.write(bytes(msg_erro, "utf-8"))


if __name__ == "__main__":
    gate = HTTPServer((GATEWAY_HOST, GATEWAY_PORT), ZTNAGateway)
    print(f"GATEWAY ZTNA ativo em http://GATEWAY_HOST}:{GATEWAY_PORT}")
    try:
        gate.serve_forever()
    except KeyboardInterrupt:
        pass
    gate.server_close()
