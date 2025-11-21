# cliente_teste.py
import urllib.request
import urllib.error

URL_GATEWAY = "http://127.0.0.1:9000"

def tentar_acesso(token=None):
    print(f"\n--- A tentar aceder com token: {token} ---")
    
    # Criação do pedido
    req = urllib.request.Request(URL_GATEWAY)
    
    if token:
        # Adiciona o nosso "Passaporte ZTNA" ao cabeçalho
        req.add_header('X-ZTNA-Token', token)
    
    try:
        resposta = urllib.request.urlopen(req)
        print("Resultado: SUCESSO! 🎉")
        print("Conteúdo recebido:")
        print(resposta.read().decode('utf-8')[:100] + "...") # Mostra só o início
    except urllib.error.HTTPError as e:
        print(f"Resultado: FALHA ⛔. Código de erro: {e.code}")

# Cenário 1: Utilizador comum (sem token / hacker)
tentar_acesso(token=None)

# Cenário 2: Utilizador com token errado
tentar_acesso(token="senha_fraca")

# Cenário 3: Utilizador Autorizado (Correto)
tentar_acesso(token="segredo_super_seguro")
