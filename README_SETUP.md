# 🚀 Guia de Setup: Spring Boot + GraphQL + MongoDB

Este guia explica como configurar e rodar a nova API de Churn Prediction.

## 1. Pré-requisitos

Antes de começar, certifique-se de ter instalado:

1. **Java 17+**: (Já instalamos o Eclipse Temurin)
2. **Docker Desktop**: (Necessário para rodar o banco de dados)
3. **Maven**: Para compilar o projeto Java.

## 2. Configurando o Banco de Dados (MongoDB)

Não precisa instalar o MongoDB no Windows! Usaremos Docker.

1. Abra um terminal na pasta `spring_graphql_mongo`.
2. Suba o banco:

    ```powershell
    docker compose up -d
    ```

3. Verifique se está rodando:

    ```powershell
    docker ps
    ```

    *(Deve aparecer um container chamado `churn_mongo_db`)*

## 3. Rodando a API (Backend)

1. No terminal, compile e rode o projeto:

    ```powershell
    mvn spring-boot:run
    ```

    *Na primeira vez, ele vai baixar a internet inteira (dependências). Relaxe e pegue um café.* ☕

2. Quando aparecer `Started ChurnGraphqlApiApplication in X.XXX seconds`, está pronto!

## 4. Testando (GraphiQL)

Acesse no seu navegador: **<http://localhost:9999/graphiql>**

### Exemplo de Mutation (Criar Análise)

Cole isso no painel da esquerda e aperte Play (▶):

```graphql
mutation {
  registrarAnalise(input: {
    clienteId: "CLI-123456",
    idade: 30,
    genero: "Masculino",
    valorMensal: 29.90,
    tempoAssinaturaMeses: 6,
    avaliacaoPlataforma: 4.5,
    
    # Novos campos V4
    avaliacaoConteudoMedia: 4.0,
    avaliacaoConteudoUltimoMes: 3.5,
    tempoMedioSessaoMin: 45,
    
    # Simulação IA
    previsao: "Vai continuar",
    probabilidade: 0.15,
    riscoAlto: false
  }) {
    id
    previsao
  }
}
```

### Exemplo de Query (Listar Tudo)

```graphql
query {
  listarAnalises {
    id
    clienteId
    previsao
    probabilidade
    riscoAlto
  }
}
```

## Solução de Problemas Comuns

* **Erro "docker não encontrado"**: Reinicie o computador após instalar o Docker Desktop.
* **Erro "mvn não encontrado"**: Instale com `winget install -e --id Apache.Maven` e reabra o terminal.
* **Porta 8080 em uso**: Se tiver outro app nessa porta, edite `src/main/resources/application.yml` e mude `server.port`.
