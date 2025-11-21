# Seminário – Zero Trust Network Access (ZTNA)

Repositório da prática do seminário de **Redes de Computadores** (UNICAP), focado em uma prova de conceito de **Zero Trust Network Access (ZTNA)** usando Python.

## 🎯 Objetivo

Implementar uma PoC simples que demonstre o princípio:

> **“Never trust, always verify” – Nunca confiar, sempre verificar.**

A ideia é mostrar que mesmo estando “dentro da rede”, o acesso a um serviço sensível só é permitido se o cliente estiver devidamente autorizado.

---

## 🧱 Arquitetura da PoC

Topologia (localhost):

- `servidor_secreto.py`  
  - Servidor HTTP em `127.0.0.1:8080`
  - Retorna uma página **CONFIDENCIAL** (simulando um servidor de RH)
  - Não faz autenticação própria (confia no gateway)

- `ztna_gateway.py`  
  - Servidor em `127.0.0.1:9000`
  - Verifica um **token** na requisição
  - Se o token for válido → faz proxy para `8080`  
  - Se for inválido/ausente → responde **HTTP 403 – ACESSO NEGADO (ZERO TRUST)**

- `cliente_teste.py`  
  - Script que envia requisições ao gateway com 3 cenários:
    - Sem token  
    - Token incorreto (`senha_fraca`)  
    - Token correto (`segredo_super_seguro`)

---

## 🔬 Experimentos

### Experimento 1 – Tokens x Resposta

Três chamadas do `cliente_teste.py`:

| Cenário | Token              | HTTP | Resultado                |
|--------:|--------------------|-----:|--------------------------|
| A       | nenhum             | 403  | acesso negado            |
| B       | `senha_fraca`      | 403  | acesso negado            |
| C       | `segredo_super_seguro` | 200 | acesso permitido + HTML confidencial |

Esse teste mostra que **só o cliente com token correto consegue chegar ao servidor secreto**.

### Experimento 2 – Porta 9000 bloqueada/liberada

1. Acesso no navegador a `http://localhost:9000` (sem token)  
   - Página vermelha de **ACESSO NEGADO (ZERO TRUST)**  
   - Logs do gateway: *Acesso BLOQUEADO* (403)

2. Execução do cliente com token/senha correta  
   - Gateway passa a aceitar a requisição  
   - Navegador em `127.0.0.1:9000/?token=...` mostra a página **CONFIDENCIAL**

Na prática, a **mesma porta 9000** parece “fechada” para usuários não autorizados e “abre” apenas para quem atende à política do gateway.

---

## ▶️ Como executar

```bash
# 1. Iniciar o servidor secreto
python servidor_secreto.py

# 2. Iniciar o gateway ZTNA
python ztna_gateway.py

# 3. Rodar o cliente de teste (3 cenários de token)
python cliente_teste.py

# 4. (Experimento 2) Acessar no navegador:
#    - Sem token:  http://localhost:9000
#    - Com token:  http://127.0.0.1:9000/?token=SEU_TOKEN
