# Guia de Segurança e Autenticação

## Visão Geral

A API agora é protegida por autenticação JWT (JSON Web Token).
O fluxo para interagir com a API mudou ligeiramente.

## Fluxo de Autenticação

1. **Cadastro (`POST /usuarios`)**: Opcional se já tiver usuário.
   - Payload: `{"login": "user", "senha": "123"}`
   - Retorno: `201 Created`

2. **Login (`POST /login`)**: Obrigatório para obter token.
   - Payload: `{"login": "user", "senha": "123"}`
   - Retorno: `{"token": "eyJhbGciOi..."}`

3. **Chamadas Protegidas (`POST /graphql`)**:
   - Header Obrigatório: `Authorization: Bearer <SEU_TOKEN>`

## Script de Teste Automatizado

Para validar todo o fluxo automaticamente, execute o script Python incluído:

```bash
python test_api_e2e.py
```

Este script realiza cadastro, login e chamadas GraphQL automaticamente.

## Fallback de Segurança

Caso a variável de ambiente `JWT_TOKEN` não seja definida, o sistema usa um segredo de fallback interno para garantir que a aplicação suba com sucesso em qualquer ambiente.
