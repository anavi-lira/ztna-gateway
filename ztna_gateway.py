from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import urllib.request

GATEWAY_HOST = "127.0.0.1"
GATEWAY_PORT = 9000

ALVO_REAL = "http://127.0.0.1:8080"
TOKEN_VALIDO = "senha_forte"

COOKIE_NAME = "ztna"
COOKIE_VALUE = "liberado"

GATEWAY_HEADER = "X-Internal-Gateway"
GATEWAY_SECRET = "ztna-ok"


class ZTNAGateway(BaseHTTPRequestHandler):
    def _cookie_liberado(self):
        cookie = self.headers.get("Cookie", "")
        return f"{COOKIE_NAME}={COOKIE_VALUE}" in cookie

    def _pagina_login(self, mensagem=""):
        html = f"""
        <html>
        <head>
            <meta charset="utf-8">
            <title>ZTNA Gateway</title>
        </head>
        <body style="font-family:Arial;text-align:center;padding-top:60px;background:#f4f6f8;">
            <h1>ZTNA Gateway</h1>
            <p>Informe o token para acessar o serviço protegido.</p>
            {f'<p style="color:red;"><b>{mensagem}</b></p>' if mensagem else ''}
            <form method="POST" action="/login">
                <input type="password" name="token" placeholder="Digite o token"
                       style="padding:10px;width:240px;font-size:16px;">
                <br><br>
                <button type="submit"
                        style="padding:10px 20px;font-size:16px;background:#007bff;color:white;border:none;border-radius:6px;">
                    Liberar acesso
                </button>
            </form>
        </body>
        </html>
        """
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

    def _pagina_acesso_liberado(self):
        html = """
        <html>
        <head>
            <meta charset="utf-8">
            <title>Acesso Liberado</title>
        </head>
        <body style="font-family:Arial;text-align:center;padding-top:60px;background:#eaffea;">
            <h1 style="color:green;">ACESSO LIBERADO</h1>
            <p>Seu acesso foi validado com sucesso pelo gateway ZTNA.</p>
            <a href="/protegido"
               style="display:inline-block;margin-top:20px;padding:12px 24px;background:green;color:white;text-decoration:none;border-radius:6px;">
               Entrar no sistema protegido
            </a>
        </body>
        </html>
        """
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.send_header("Set-Cookie", f"{COOKIE_NAME}={COOKIE_VALUE}; Path=/")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

    def _pagina_negado(self):
        html = """
        <html>
        <head>
            <meta charset="utf-8">
            <title>Acesso Negado</title>
        </head>
        <body style="font-family:Arial;text-align:center;padding-top:60px;background:#ffe6e6;">
            <h1 style="color:red;">ACESSO NEGADO</h1>
            <p>Token inválido ou ausente.</p>
            <a href="/" style="display:inline-block;margin-top:20px;">Voltar</a>
        </body>
        </html>
        """
        self.send_response(403)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

    def _encaminhar_servidor_secreto(self):
        try:
            req = urllib.request.Request(
                ALVO_REAL,
                headers={GATEWAY_HEADER: GATEWAY_SECRET}
            )
            with urllib.request.urlopen(req) as resposta:
                conteudo = resposta.read()

            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(conteudo)
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(f"Erro ao acessar servidor protegido: {e}".encode("utf-8"))

    def do_GET(self):
        if self.path == "/":
            self._pagina_login()
            return

        if self.path == "/protegido":
            if self._cookie_liberado():
                self._encaminhar_servidor_secreto()
            else:
                self._pagina_negado()
            return

        self.send_response(404)
        self.end_headers()

    def do_POST(self):
        if self.path != "/login":
            self.send_response(404)
            self.end_headers()
            return

        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8")
        params = parse_qs(body)
        token = params.get("token", [""])[0]

        if token == TOKEN_VALIDO:
            self._pagina_acesso_liberado()
        else:
            self._pagina_login("Token inválido.")

if __name__ == "__main__":
    gateway = HTTPServer((GATEWAY_HOST, GATEWAY_PORT), ZTNAGateway)
    print(f"Gateway ZTNA rodando em http://{GATEWAY_HOST}:{GATEWAY_PORT}")
    try:
        gateway.serve_forever()
    except KeyboardInterrupt:
        pass
    gateway.server_close()
