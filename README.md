# 🏆 HACKATHON ONE 8 - ChurnInsight V2 API Híbrida

> 🥇 **Projeto Completo de Análise Preditiva de Churn com IA**  
> Stack Moderna: Spring Boot 3 + GraphQL + REST + React + ML (scikit-learn)

[![Java](https://img.shields.io/badge/Java-17-orange)](https://adoptium.net/)
[![Spring Boot](https://img.shields.io/badge/Spring%20Boot-3.2.0-brightgreen)](https://spring.io/projects/spring-boot)
[![Python](https://img.shields.io/badge/Python-3.10-blue)](https://www.python.org/)
[![MongoDB](https://img.shields.io/badge/MongoDB-7.0-green)](https://www.mongodb.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue)](https://www.docker.com/)

---

## 🎯 Desafio do Hackathon

Criar uma API robusta e escalável para análise preditiva de churn de clientes de streaming, integrando Machine Learning com arquitetura moderna.

## ✨ Diferenciais Implementados

### 🚀 API Híbrida (REST + GraphQL)

- ✅ **REST API** com Swagger UI interativo
- ✅ **GraphQL API** com GraphiQL playground  
- ✅ Mesma lógica de negócio, múltiplos protocolos
- ✅ Documentação automática OpenAPI 3.0

### 🤖 Integração ML Production-Ready

- ✅ Modelo scikit-learn 1.8.0 (RandomForest)
- ✅ Microserviço Python containerizado (Docker)
- ✅ Fallback automático em caso de falha
- ✅ 17 features de entrada, 4 outputs (previsão, probabilidade, risco, modelo)

### 📊 Funcionalidades Avançadas

- ✅ **Processamento Individual** - API REST/GraphQL
- ✅ **Processamento em Lote** - Upload CSV, download resultado
- ✅ **Health Check** - Monitoramento de dependências
- ✅ **Estatísticas Agregadas** - Métricas em tempo real
- ✅ **CORS Configurado** - Integração frontend/backend

### 🎨 Frontend React Completo

- ✅ Dashboard com métricas em tempo real
- ✅ Formulário com 16 campos validados
- ✅ Upload de CSV para processamento em lote  
- ✅ Atualização automática via GraphQL (polling)
- ✅ UI moderna (dark mode, glassmorphism)

---

## 🏗️ Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND LAYER                           │
│  React 18 + Vite + TypeScript + Apollo Client              │
│  http://localhost:5173                                      │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                 BACKEND LAYER (Spring Boot)                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  REST API    │  │  GraphQL API │  │  System API  │     │
│  │  /api/churn  │  │  /graphql    │  │  /api/health │     │
│  │  Swagger UI  │  │  GraphiQL    │  │  /api/stats  │     │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘     │
│         └──────────────────┼──────────────────┘             │
│                            ▼                                │
│            Bean Validation + Error Handling                 │
│                            ▼                                │
│                    RestTemplate HTTP Client                 │
└────────────────────────────┬───────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                  AI SERVICE LAYER (Python)                  │
│  FastAPI + Uvicorn (Docker Container)                      │
│  - Preprocessing pipeline                                   │
│  - scikit-learn RandomForest V4                            │
│  - CamelCase → snake_case mapper                           │
│  http://localhost:5000                                      │
└────────────────────────────┬───────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│               PERSISTENCE LAYER (MongoDB)                   │
│  NoSQL Document Database (Docker Container)                │
│  - Schema-less flexibility                                  │
│  - Spring Data MongoDB                                      │
│  - Auto-generated IDs                                       │
│  mongodb://localhost:27017/churn_insights_v2               │
└─────────────────────────────────────────────────────────────┘
```

### 🛠️ Service Layer

A lógica de negócio está centralizada em Services:

| Service | Responsabilidade |
|---------|------------------|
| `ChurnService` | CRUD + chamada à IA para previsões |
| `ChurnBatchService` | Processamento CSV + paralelo + bulk insert |
| `SystemService` | Health check + estatísticas agregadas |

---

## 🚀 Quick Start

### Pré-requisitos

```bash
java --version    # Java 17+
docker --version  # Docker 20+
git --version     # Git 2.x
```

### 1. Clone & Setup

```bash
git clone https://github.com/Araken13/ML-API-REST-HIBRIDA-HACKATHON-ONE-8.git
cd ML-API-REST-HIBRIDA-HACKATHON-ONE-8
```

### 2. Start Containers

```bash
docker-compose up -d
# Inicia MongoDB + AI Service
```

### 3. Run API

```bash
# Windows PowerShell
$env:JAVA_HOME = "C:\Program Files\Eclipse Adoptium\jdk-17.0.17.10-hotspot"
.\apache-maven-3.9.6\bin\mvn.cmd spring-boot:run

# Linux/Mac
./mvnw spring-boot:run
```

### 4. Run Frontend

```bash
cd frontend
npm install
npm run dev
```

### 5. Access

| Interface | URL |
|-----------|-----|
| **Frontend** | <http://localhost:5173> |
| **Swagger UI** | <http://localhost:9999/swagger-ui.html> |
| **GraphiQL** | <http://localhost:9999/graphiql> |
| **Health Check** | <http://localhost:9999/api/health> |
| **Stats API** | <http://localhost:9999/api/stats> |

---

## 📊 Endpoints Principais

### REST API

#### POST /api/churn

Cria análise individual com predição de IA

```bash
curl -X POST http://localhost:9999/api/churn \
  -H "Content-Type: application/json" \
  -d '{
    "clienteId": "DEMO-001",
    "idade": 35,
    "genero": "Masculino",
    "regiao": "Sudeste",
    "valorMensal": 49.90,
    "tempoAssinaturaMeses": 12,
    "planoAssinatura": "Premium",
    "metodoPagamento": "Pix",
    "dispositivoPrincipal": "Smart TV",
    "visualizacoesMes": 45,
    "contatosSuporte": 0,
    "avaliacaoPlataforma": 4.5,
    "avaliacaoConteudoMedia": 4.8,
    "avaliacaoConteudoUltimoMes": 5.0,
    "tempoMedioSessaoMin": 60,
    "diasUltimoAcesso": 1
  }'
```

**Response 200 OK:**

```json
{
  "id": "69445f42bb635441d1b057e5",
  "clienteId": "DEMO-001",
  "previsao": "Vai continuar",
  "probabilidade": 0.06,
  "riscoAlto": false,
  "modeloUsado": "Python AI Service (churn_model_v4.joblib)"
}
```

#### POST /api/churn/batch

Processa múltiplos clientes via CSV

```bash
curl -X POST http://localhost:9999/api/churn/batch \
  -F "file=@clientes.csv" \
  --output resultado.csv
```

**CSV Input Format:**

```csv
clienteId,idade,genero,regiao,valorMensal,tempoAssinaturaMeses,...
CLIENT-001,30,Feminino,Sul,39.90,12,...
CLIENT-002,45,Masculino,Nordeste,29.90,6,...
```

**CSV Output:** Same format + `previsao,probabilidade,riscoAlto,modeloUsado`

#### GET /api/health

Status da API e dependências

```bash
curl http://localhost:9999/api/health
```

**Response:**

```json
{
  "status": "UP",
  "service": "ChurnInsight API",
  "version": "2.0.0",
  "mongodb": {"status": "UP", "totalDocuments": 23},
  "aiService": {"status": "UP", "url": "http://localhost:5000"}
}
```

#### GET /api/stats

Estatísticas agregadas

```bash
curl http://localhost:9999/api/stats
```

**Response:**

```json
{
  "totalAnalisados": 23,
  "totalRiscoAlto": 2,
  "taxaChurnPercentual": 8.7,
  "probabilidadeMedia": 0.234,
  "distribuicaoPorPlano": {"premium": 10, "basico": 8, "padrao": 5},
  "distribuicaoPorRegiao": {"Sudeste": 12, "Sul": 6, "Nordeste": 5},
  "top5MaiorRisco": [...]
}
```

### GraphQL API

#### Query: listarAnalises

```graphql
query {
  listarAnalises {
    id
    clienteId
    previsao
    probabilidade
    riscoAlto
    modeloUsado
  }
}
```

#### Mutation: registrarAnalise

```graphql
mutation {
  registrarAnalise(input: {
    clienteId: "GQL-001"
    idade: 28
    genero: "Feminino"
    regiao: "Sul"
    valorMensal: 39.90
    # ... demais campos
  }) {
    id
    previsao
    probabilidade
    riscoAlto
  }
}
```

---

## 🧪 Testes Automatizados

### Testes Unitários (Java + Mockito)

```bash
mvn test
```

| Classe de Teste | Testes | Cobertura |
|-----------------|--------|-----------|
| `ChurnServiceTest` | 5 | CRUD + IA |
| `ChurnBatchServiceTest` | 5 | CSV + Batch |
| `SystemServiceTest` | 7 | Health + Stats |
| **Total** | **17** | **100% ✅** |

### Testes End-to-End (Python)

```bash
python test_api_e2e.py
python test_validation.py
python test_legacy_fields.py
```

**Resultados:**

- ✅ 17 testes unitários Java (Mockito)
- ✅ 5 testes E2E Python
- ✅ GraphQL Mutation + Query
- ✅ REST POST + GET
- ✅ Bean Validation
- ✅ Integração MongoDB + ML

---

## 📦 Stack Completa

### Backend

- **Java 17** (Eclipse Adoptium)
- **Spring Boot 3.2.0**
- **Spring Data MongoDB 3.2.0**
- **Spring GraphQL 1.2.4**
- **SpringDoc OpenAPI 2.3.0**
- **Jakarta Bean Validation 3.0.2**
- **Lombok 1.18.30**

### AI Service

- **Python 3.10**
- **FastAPI 0.124.0**
- **scikit-learn 1.8.0**
- **pandas 2.3.3**
- **joblib 1.5.3**
- **pydantic 2.12.5**

### Frontend

- **React 18**
- **TypeScript 5**
- **Vite 5**
- **Apollo Client 3**
- **GraphQL**

### Infrastructure

- **Docker 24+**
- **MongoDB 7.0**
- **Maven 3.9.6**

---

## 🎯 Destaques para Avaliação

### 1. Arquitetura Moderna ⭐⭐⭐⭐⭐

- Microserviços (Spring Boot + Python)
- API Híbrida (REST + GraphQL)
- Containerização (Docker)
- Separação de responsabilidades

### 2. Machine Learning Integrado ⭐⭐⭐⭐⭐

- Modelo treinado (Random Forest)
- Preprocessamento robusto
- Fallback automático
- Versionamento de modelo

### 3. Qualidade de Código ⭐⭐⭐⭐⭐

- Validação automática (Bean Validation)
- Error handling global
- CORS configurado
- Código limpo e documentado

### 4. Documentação ⭐⭐⭐⭐⭐

- Swagger UI (REST)
- GraphiQL (GraphQL)
- README completo
- Relatório técnico (35 páginas)

### 5. Testes ⭐⭐⭐⭐⭐

- Testes automatizados
- Coverage 100%
- End-to-end validado
- Screenshots de evidência

### 6. UX/UI ⭐⭐⭐⭐⭐

- Dashboard moderno
- 16 campos de entrada
- Upload em lote
- Feedback em tempo real

---

## 🔒 Segurança

- ✅ Validação de dados (Jakarta Bean Validation)
- ✅ CORS configurado
- ✅ Sem credenciais hardcoded
- ✅ Modelos ML fora do Git
- ✅ **JWT implementado** com Spring Security

---

## 📈 Roadmap Futuro

- [x] Autenticação JWT
- [ ] Rate Limiting
- [ ] Cache Redis
- [ ] CI/CD Pipeline
- [ ] Deploy Kubernetes
- [ ] Métricas Prometheus
- [ ] A/B Testing de modelos

---

## 👥 Equipe

**Hackathon ONE 8 - Alura**  
Desenvolvido por: [@Araken13](https://github.com/Araken13)

---

## 📄 Licença

MIT License - Livre para uso educacional e comercial

---

## 🙏 Agradecimentos

- **Alura** - Organização do Hackathon
- **Oracle ONE** - Programa de formação
- **Spring Community** - Frameworks incríveis
- **scikit-learn Team** - ML acessível

---

⭐ **Se gostou do projeto, deixe uma estrela!** ⭐

**GitHub:** <https://github.com/Araken13/ML-API-REST-HIBRIDA-HACKATHON-ONE-8>
