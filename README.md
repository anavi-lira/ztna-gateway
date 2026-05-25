# ZTNA Gateway — Prova de Conceito em Python

Projeto de demonstração prática de **ZTNA (Zero Trust Network Access)**, desenvolvido em Python, com foco em ilustrar o princípio de segurança:

> **Never trust, always verify**  
> **Nunca confiar automaticamente, sempre verificar.**

A proposta do projeto é mostrar, de forma simples, como um **gateway de acesso** pode proteger um serviço interno sensível, permitindo acesso apenas a usuários autorizados.

---

## Objetivo

Demonstrar, em uma prova de conceito, como o modelo **Zero Trust** pode ser aplicado ao acesso a aplicações internas.

No projeto:

- o serviço protegido **não deve ser acessado diretamente**;
- o acesso deve passar por um **gateway ZTNA**;
- o gateway valida se o cliente está autorizado;
- apenas após essa verificação o conteúdo confidencial é liberado.

---

## Conceitos usados

### ZTA — Zero Trust Architecture
É a arquitetura geral de segurança baseada no princípio de que nenhum usuário, dispositivo ou requisição deve ser confiado automaticamente.

### ZTNA — Zero Trust Network Access
É uma aplicação prática da ZTA, focada em **controle de acesso a serviços e aplicações de rede**.

Neste projeto, o **gateway** funciona como o mecanismo de ZTNA.

---

## Estrutura do projeto

### `servidor_secreto.py`
Simula um serviço interno sensível.

Função:
- hospedar um conteúdo confidencial;
- responder apenas quando o acesso vier corretamente por meio do gateway.

Exemplo de conteúdo:
- “dados confidenciais”
- informação sensível simulada, como salário do CEO

---

### `ztna_gateway.py`
É o componente principal da prova de conceito.

Função:
- receber o acesso do usuário;
- validar token/autorização;
- liberar ou bloquear o acesso;
- encaminhar a requisição ao servidor protegido apenas quando permitido.

É o elemento que representa o controle de acesso baseado em **Zero Trust**.

---

## Fluxo da aplicação

1. O usuário tenta acessar o gateway.
2. O gateway verifica se o acesso está autorizado.
3. Se não estiver autorizado:
   - o acesso é negado.
4. Se estiver autorizado:
   - o gateway libera a entrada;
   - o conteúdo do servidor protegido passa a ser exibido.

---

## Arquitetura simplificada

```text
Usuário/Navegador
        |
        v
   ZTNA Gateway  ---- valida acesso ----> se autorizado
        |
        v
Servidor Secreto (protegido)
