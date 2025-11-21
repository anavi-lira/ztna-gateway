from http.server import BaseHTTPRequestHandler, HTTPServer

# Configurações
HOST = "127.0.0.1"
PORT = 8080


class MeuServidorSecreto(BaseHTTPRequestHandler):
    def do_GET(self):
        # Quando alguém acede, envia esta resposta
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()

        mensagem = """
        <html>
        <body style="background-color: #e0ffe0;">
        <h1>CONFIDENCIAL</h1>
        <p>Parabéns! Chegaste ao servidor de RH.</p>
        <p>Dados sensíveis: O salário do CEO é 1.000.000€</p>
        </body>
        </html>
        """
        self.wfile.write(bytes(mensagem, "utf-8"))


if __name__ == "__main__":
    servidor = HTTPServer((HOST, PORT), MeuServidorSecreto)
    print(f" SERVIDOR SECRETO ativo em http://{HOST}:{PORT}")
    print("Este servidor não deve ser acedido diretamente, mas sim pelo Gateway ZTNA.")
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        pass
    servidor.server_close()
