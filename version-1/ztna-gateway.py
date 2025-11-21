# ztna_gateway.py
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.request

# O Gateway corre numa porta diferente (pública)
GATEWAY_HOST = "127.0.0.1"
GATEWAY_PORT = 9000

# Onde está o servidor real (escondido)
ALVO_REAL = "http://127.0.0.1:8080"

class ZTNAGateway(BaseHTTPRequestHandler):
    
    def verificar_postura(self):
        """
        Simulação ZTNA: Verifica cabeçalhos ou tokens.
        Aqui vamos simular que o browser envia um 'Token' especial.
        Na vida real, isto seria um certificado de máquina ou login SSO.
        """
        # Vamos procurar um cabeçalho falso chamado 'X-ZTNA-Token'
        token = self.headers.get('X-ZTNA-Token')
        
        # A Regra: Só entra quem tem o token 'segredo_super_seguro'
        if token == "segredo_super_seguro":
            return True
        return False

    def do_GET(self):
        print(f"--- Pedido recebido de: {self.client_address} ---")
        
        # 1. APLICAÇÃO DA POLÍTICA ZERO TRUST
        acesso_permitido = self.verificar_postura()

        if acesso_permitido:
            print("✅ Acesso PERMITIDO. A contactar o servidor real...")
            try:
                # O Gateway vai buscar os dados ao servidor secreto (Proxy)
                resposta_real = urllib.request.urlopen(ALVO_REAL)
                conteudo = resposta_real.read()
                
                # Envia os dados para o utilizador
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(conteudo)
                
            except Exception as e:
                self.send_error(500, f"Erro ao contactar servidor secreto: {e}")
        
        else:
            print("❌ Acesso BLOQUEADO (Falta token ou token inválido).")
            # Resposta de erro personalizada
            self.send_response(403) # 403 Forbidden
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            msg_erro = """
            <html>
            <body style="background-color: #ffe0e0; color: red;">
                <h1>⛔ ACESSO NEGADO (ZERO TRUST)</h1>
                <p>O teu dispositivo não foi verificado ou não tens autorização.</p>
                <p>Falta o cabeçalho: X-ZTNA-Token</p>
            </body>
            </html>
            """
            self.wfile.write(bytes(msg_erro, "utf-8"))

if __name__ == "__main__":
    gate = HTTPServer((GATEWAY_HOST, GATEWAY_PORT), ZTNAGateway)
    print(f"🛡️ GATEWAY ZTNA ativo em http://{GATEWAY_HOST}:{GATEWAY_PORT}")
    print("Acede a este endereço no teu browser.")
    try:
        gate.serve_forever()
    except KeyboardInterrupt:
        pass
    gate.server_close()
