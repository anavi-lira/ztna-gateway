import urllib.request
import urllib.error

URL_GATEWAY = "http://127.0.0.1:9000"


def tentar_acesso(token=None):
    print(f"\n--- A tentar aceder com token: {token} ---")
    req = urllib.request.Request(URL_GATEWAY)

    if token:
        req.add_header('X-ZTNA-Token', token)

    try:
        resposta = urllib.request.urlopen(req)
        print("Resultado: SUCESSO!")
        print("Abra no navegador esta URL para ficar autorizado:")
        print("http://127.0.0.1:9000/?token=senha_forte")
        # Se quiser ver o HTML:
        # print(resposta.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"Resultado: FALHA. Código de erro: {e.code}")


# Cenário 3 — desbloqueia navegador
if __name__ == "__main__":
    tentar_acesso(token="senha_forte")
