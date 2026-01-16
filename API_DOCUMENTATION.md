# 📘 Documentação Oficial da API ChurnInsight v2.0

> **Sua solução Enterprise para Previsão de Rotatividade de Clientes com Inteligência Artificial.**

Bem-vindo à documentação da API **ChurnInsight**. Esta plataforma oferece uma solução robusta e híbrida (REST + GraphQL) para análise de rotatividade de clientes (Churn), desenvolvida para escalar com seu negócio.

---

## 📑 Tabela de Conteúdos

1. [Visão Geral](#-visão-geral)
2. [Arquitetura e Tecnologias](#️-arquitetura-e-tecnologias)
3. [Diferenciais de Negócio](#-lógica-da-aplicação-e-diferenciais)
4. [Guia Rápido (Quick Start)](#-guia-rápido-quick-start)
5. [Autenticação](#-autenticação)
6. [API REST - Individual](#-api-rest---análise-individual)
7. [API REST - Batch (Lote)](#-processamento-em-lote-batch)
8. [API GraphQL](#-graphql-api)
9. [Dicionário de Erros](#-dicionário-de-códigos-http)
10. [Glossário de Dados](#-glossário-de-campos-importantes)

---

## 🚀 Visão Geral

A **ChurnInsight API** permite que empresas integrem capacidades preditivas em seus sistemas legados ou aplicações modernas.

- **Base URL**: `http://localhost:9999` (Ambiente Local)
- **Formatos Suportados**: JSON, Multipart (CSV)
- **Protocolos**: RESTful, GraphQL
- **Autenticação**: JWT (JSON Web Token)

### Exemplo: Buscar por ID

```graphql
query {
  buscarPorId(id: "uuid-do-cliente") {
    id
    clienteId
    previsao
    modeloUsado
  }
}
```

### Exemplo: Mutation

---

## 🏗️ Arquitetura e Tecnologias

Sistema construído seguindo princípios **Cloud-Native** e **Arquitetura Hexagonal**.

### 🔧 Backend (Core)

- **Framework**: Spring Boot 3.2 (Java 17) para robustez.
- **Segurança**: Spring Security com JWT Stateless.
- **Persistência**: Spring Data JPA.
- **Documentação**: SpringDoc OpenAPI 3.

### 🧠 Microserviço de IA

- **Framework**: FastAPI (Python) para baixa latência.
- **Libs**: Scikit-Learn e Pandas.
- **Modelo**: Random Forest otimizado para classificação binária.

### ☁️ Infraestrutura

- **Containerização**: Docker e Docker Compose.
- **Performance**: Processamento assíncrono e multi-threading para grandes volumes.

---

## 🧠 Lógica da Aplicação e Diferenciais

### 1. 🔄 Híbrido por Design

Suporte simultâneo a **REST** (para integrações backend-to-backend simples) e **GraphQL** (para frontends modernos como React/Vue), evitando *over-fetching*.

### 2. ⚡ Batch Processing Otimizado

O upload de CSVs utiliza um **Pipeline Paralelo**:

1. O CSV é "streamado" e fatiado em memória.
2. Workers (threads) enviam lotes simultâneos para a IA.
3. Resposta gerada em tempo real.
*Performance*: ~50.000 registros processados em poucos minutos.

### 3. 🛡️ IA Explicável (XAI)

Não retornamos apenas "Churn/Não Churn". O modelo entrega:

- **Probabilidade (%)**: Nível de certeza.
- **Risco**: Classificação (Alto/Baixo) baseada em regras de negócio ajustáveis.

---

## 🏁 Guia Rápido (Quick Start)

Suba o ambiente completo em 3 passos usando Docker:

**1. Clone o repositório**

```bash
git clone https://github.com/SeuRepo/hackathon_g8_one.git
cd hackathon_g8_one
```

**2. Inicie os containers**

```bash
docker-compose up --build -d
```

**3. Teste a saúde da API**

```bash
curl http://localhost:9999/api/health
```

---

## 🔐 Autenticação

Todos os endpoints de negócio são protegidos. Você precisa obter um token `Bearer`.

### 1. Criar Usuário Admin

- **POST** `/usuarios`

```bash
curl -X POST http://localhost:9999/usuarios \
  -H "Content-Type: application/json" \
  -d '{"login": "admin", "senha": "123"}'
```

### 2. Login (Gerar Token)

- **POST** `/login`

```bash
curl -X POST http://localhost:9999/login \
  -H "Content-Type: application/json" \
  -d '{"login": "admin", "senha": "123"}'
```

> **Resposta**: Guarde o valor de `token` retornado.

---

## 📡 API REST - Análise Individual

Para integrações pontuais (ex: verificar risco ao abrir chamado de suporte).

### Nova Previsão

- **POST** `/api/churn`
- **Header**: `Authorization: Bearer <SEU_TOKEN>`

**Payload Completo:**

```json
{
  "clienteId": "CLI-001",
  "idade": 30,
  "genero": "Masculino",
  "regiao": "Sudeste",
  "valorMensal": 49.90,
  "tempoAssinaturaMeses": 12,
  "diasUltimoAcesso": 2,
  "avaliacaoPlataforma": 4.5,
  "avaliacaoConteudoMedia": 4.0,
  "avaliacaoConteudoUltimoMes": 4.2,
  "tempoMedioSessaoMin": 45,
  "planoAssinatura": "Padrao",
  "metodoPagamento": "Credito",
  "dispositivoPrincipal": "Mobile",
  "visualizacoesMes": 15,
  "contatosSuporte": 1,
  "tipoContrato": "ANUAL",
  "categoriaFavorita": "FILMES",
  "acessibilidade": 0
}
```

---

## 📦 Processamento em Lote (Batch)

Ideal para processamento noturno ou cargas massivas de dados históricos.

### Upload Otimizado

- **POST** `/api/churn/batch/optimized`
- **Header**: `Authorization: Bearer <SEU_TOKEN>`
- **Body**: `multipart/form-data` (key: `file`)

**Exemplo:**

```bash
curl -X POST http://localhost:9999/api/churn/batch/optimized \
  -H "Authorization: Bearer <TOKEN>" \
  -F "file=@base_clientes.csv" > resultado.csv
```

---

## ⚛️ GraphQL API

Ponto único de entrada para consultas flexíveis.

- **Endpoint**: `/graphql`

### Exemplo: Dashboard de Risco

Recupere apenas clientes de alto risco para exibir em um dashboard administrativo.

```graphql
query {
  listarRiscoAlto {
    clienteId
    probabilidade
    planoAssinatura
    valorMensal
  }
}
```

### Exemplo: Mutation

```graphql
mutation {
  registrarAnalise(input: {
    clienteId: "CLI-GQL-1",
    idade: 25,
    genero: "Feminino",
    regiao: "Norte",
    valorMensal: 29.90,
    tempoAssinaturaMeses: 3,
    diasUltimoAcesso: 10,
    avaliacaoPlataforma: 4,
    avaliacaoConteudoMedia: 4,
    avaliacaoConteudoUltimoMes: 3,
    tempoMedioSessaoMin: 20,
    planoAssinatura: "Basico",
    metodoPagamento: "Pix",
    dispositivoPrincipal: "Mobile",
    visualizacoesMes: 5,
    contatosSuporte: 1,
    tipoContrato: "MENSAL",
    categoriaFavorita: "ESPORTES",
    acessibilidade: 1
  }) {
    id
    previsao
    probabilidade
  }
}
```

---

## � Dicionário de Códigos HTTP

Listagem dos principais status retornados pela API:

| Código | Status | Descrição |
| :--- | :--- | :--- |
| `200` | OK | Requisição processada com sucesso. |
| `201` | Created | Recurso criado com sucesso (ex: novo usuário). |
| `400` | Bad Request | Erro de validação nos dados enviados (ex: idade negativa). |
| `401` | Unauthorized | Falha na autenticação (senha incorreta). |
| `403` | Forbidden | Token ausente, inválido ou expirado. |
| `500` | Internal Server Error | Erro inesperado no servidor ou falha na comunicação com IA. |

---

## 📖 Glossário de Campos Importantes

Entenda as variáveis que influenciam o modelo de IA:

- **diasUltimoAcesso**: Quantos dias faz que o usuário não loga na plataforma. (Alto impacto no Churn)
- **avaliacaoConteudoUltimoMes**: Nota média (0-5) dada aos conteúdos no último mês. Quedas bruscas indicam risco.
- **contatosSuporte**: Número de chamados abertos. Muitos chamados podem indicar frustração.
- **tipoContrato**: "Mensal" tem maior volatilidade que "Anual".

---

## 📊 Monitoramento

- `GET /api/health`: Healthcheck (UP/DOWN)
- `GET /api/stats`: Estatísticas de uso da API.

---
*© 2026 Hackathon Team G8 One. All rights reserved.*
