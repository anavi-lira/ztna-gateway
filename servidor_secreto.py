from http.server import BaseHTTPRequestHandler, HTTPServer

HOST = "127.0.0.1"
PORT = 8080
GATEWAY_HEADER = "X-Internal-Gateway"
GATEWAY_SECRET = "ztna-ok"


class ServidorSecreto(BaseHTTPRequestHandler):
    def do_GET(self):
        gateway_auth = self.headers.get(GATEWAY_HEADER)

        if gateway_auth != GATEWAY_SECRET:
            self.send_response(403)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()

            html = """
            <html>
            <head><meta charset="utf-8"><title>Acesso Proibido</title></head>
            <body style="font-family:Arial;text-align:center;padding-top:60px;background:#ffe6e6;">
                <h1 style="color:red;">ACESSO PROIBIDO</h1>
                <p>Este servidor interno não pode ser acessado diretamente.</p>
                <p>Utilize o gateway ZTNA para solicitar acesso.</p>
            </body>
            </html>
            """
            self.wfile.write(html.encode("utf-8"))
            return

        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()

        html = """
        <html>
        <head><meta charset="utf-8"><title>Servidor Secreto</title></head>
        <body style="font-family:Arial;text-align:center;padding-top:60px;background:#f0fff0;">
            <h1 style="color:green;">DADOS CONFIDENCIAIS</h1>
            <p>Salário do CEO: R$ 120.000,00</p>
            <p>Bônus anual: R$ 300.000,00</p>
        </body>
        </html>
        """
        self.wfile.write(html.encode("utf-8"))


if __name__ == "__main__":
    server = HTTPServer((HOST, PORT), ServidorSecreto)
    print(f"Servidor secreto rodando em http://{HOST}:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()
