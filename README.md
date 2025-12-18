# 🚀 ML API REST Híbrida - ChurnInsight V2

API Híbrida (REST + GraphQL) desenvolvida em **Spring Boot 3** com integração de Machine Learning para previsão de Churn de clientes de streaming.

## 📋 Sobre o Projeto

Sistema completo de análise preditiva de churn construído com arquitetura moderna e escalável, combinando:

- **Backend Java**: Spring Boot 3.2.0 com GraphQL e REST
- **AI Service**: Python 3.10 com scikit-learn (containerizado)
- **Database**: MongoDB (NoSQL)
- **Infraestrutura**: Docker, Maven

## 🏗️ Arquitetura

```
┌─────────────────────┐
│  Frontend React     │ (Porta 5173)
│  ChurnInsight V2    │
└──────────┬──────────┘
           │ GraphQL/REST
           ▼
┌─────────────────────┐
│  Spring Boot API    │ (Porta 9999)
│  ├─ GraphQL (/graphql)
│  ├─ REST (/api/churn)
│  └─ Swagger UI      │
└──────────┬──────────┘
           │ HTTP
           ▼
┌─────────────────────┐
│ Python AI Service   │ (Porta 5000 - Docker)
│ scikit-learn 1.8.0  │
│ FastAPI + Uvicorn   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   MongoDB           │ (Porta 27017 - Docker)
│   churn_insights_v2 │
└─────────────────────┘
```

## ✨ Funcionalidades

### API REST

- ✅ **POST** `/api/churn` - Criar nova análise com previsão de IA
- ✅ **GET** `/api/churn` - Listar todas as análises
- ✅ **GET** `/api/churn/{id}` - Buscar análise por ID
- ✅ **Swagger UI** - Documentação interativa em `/swagger-ui.html`

### API GraphQL

- ✅ **Query** `listarAnalises` - Lista todas as análises
- ✅ **Query** `listarRiscoAlto` - Filtra apenas clientes de alto risco
- ✅ **Query** `buscarPorId(id: ID!)` - Busca específica
- ✅ **Mutation** `registrarAnalise(input: ChurnInput!)` - Cria análise com IA
- ✅ **GraphiQL** - Playground interativo em `/graphiql`

### Validação de Dados

- `@NotBlank`, `@Min`, `@Max` - Validação Jakarta Bean Validation
- Rejeição automática de dados inválidos antes do processamento

### Modelo de IA (V4)

- **Algoritmo**: RandomForest / Pipeline scikit-learn
- **Features**: 17 campos (idade, plano, engagement, avaliações, dispositivos...)
- **Output**: Probabilidade de churn (0-1), classificação binária, flag de risco

## 🚀 Como Executar

### Pré-requisitos

- **Java 17+** (Eclipse Adoptium recomendado)
- **Docker Desktop** (para MongoDB e AI Service)
- **Maven 3.9+** (incluído no projeto)
- **Git**

### 1️⃣ Clone o Repositório

```bash
git clone https://github.com/Araken13/ML-API-REST-HIBRIDA-HACKATHON-ONE-8.git
cd ML-API-REST-HIBRIDA-HACKATHON-ONE-8
```

### 2️⃣ Inicie os Containers Docker

```bash
docker-compose up -d
```

Isso iniciará:

- MongoDB (porta 27017)
- Python AI Service (porta 5000)

### 3️⃣ Execute a API Spring Boot

**Windows:**

```powershell
$env:JAVA_HOME = "C:\Program Files\Eclipse Adoptium\jdk-17.0.17.10-hotspot"
.\apache-maven-3.9.6\bin\mvn.cmd spring-boot:run
```

**Linux/Mac:**

```bash
./mvnw spring-boot:run
```

### 4️⃣ Acesse as Interfaces

| Serviço | URL | Descrição |
|---------|-----|-----------|
| **Swagger UI** | <http://localhost:9999/swagger-ui.html> | Documentação REST interativa |
| **GraphiQL** | <http://localhost:9999/graphiql> | Playground GraphQL |
| **API REST** | <http://localhost:9999/api/churn> | Endpoint principal REST |
| **API GraphQL** | <http://localhost:9999/graphql> | Endpoint GraphQL |

## 📝 Exemplo de Uso

### REST (via cURL)

```bash
curl -X POST http://localhost:9999/api/churn \
  -H "Content-Type: application/json" \
  -d '{
    "clienteId": "CLIENT-001",
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

### GraphQL (via GraphiQL)

```graphql
mutation {
  registrarAnalise(input: {
    clienteId: "CLIENT-002"
    idade: 28
    genero: "Feminino"
    regiao: "Sul"
    valorMensal: 29.90
    tempoAssinaturaMeses: 6
    planoAssinatura: "Basico"
    metodoPagamento: "Credito"
    dispositivoPrincipal: "Mobile"
    visualizacoesMes: 20
    contatosSuporte: 2
    avaliacaoPlataforma: 3.5
    avaliacaoConteudoMedia: 3.0
    avaliacaoConteudoUltimoMes: 2.5
    tempoMedioSessaoMin: 30
    diasUltimoAcesso: 5
  }) {
    id
    clienteId
    previsao
    probabilidade
    riscoAlto
    modeloUsado
  }
}
```

## 🧪 Testes

O projeto inclui scripts de teste Python:

```bash
# Teste End-to-End completo
python test_api_e2e.py

# Teste de validação de dados
python test_validation.py

# Teste de campos legados (compatibilidade V1)
python test_legacy_fields.py
```

## 📦 Estrutura do Projeto

```
spring_graphql_mongo/
├── src/main/java/com/hackathon/churn/
│   ├── ChurnData.java              # Entidade MongoDB
│   ├── ChurnRepository.java        # Repository Spring Data
│   ├── ChurnController.java        # Controller GraphQL
│   ├── ChurnRestController.java    # Controller REST
│   └── ChurnGraphqlApiApplication.java
├── src/main/resources/
│   ├── graphql/schema.graphqls     # Schema GraphQL
│   └── application.yml             # Configurações Spring
├── ai_service/                     # Microserviço Python
│   ├── server.py                   # FastAPI server
│   ├── processing.py               # Preprocessamento dados
│   ├── requirements.txt            # Dependências Python
│   └── Dockerfile                  # Container AI
├── docker-compose.yml              # Orquestração containers
├── pom.xml                         # Dependências Maven
└── README.md                       # Este arquivo
```

## 🛠️ Tecnologias Utilizadas

### Backend

- Spring Boot 3.2.0
- Spring Data MongoDB
- Spring GraphQL
- SpringDoc OpenAPI (Swagger)
- Jakarta Bean Validation
- Lombok

### AI Service

- Python 3.10
- FastAPI
- Uvicorn
- scikit-learn 1.8.0
- pandas
- joblib

### Infraestrutura

- Docker & Docker Compose
- MongoDB 7.0
- Maven 3.9.6

## 🔐 Segurança

- ✅ Validação de dados em todas as camadas
- ✅ Sem credenciais hardcoded
- ✅ Modelos ML (.joblib) não versionados no Git
- ✅ CORS configurado (ajustar para produção)
- ⚠️ Em produção, configure autenticação/autorização (JWT, OAuth2)

## 📊 Melhorias Futuras

- [ ] Autenticação JWT
- [ ] Rate Limiting
- [ ] Cache com Redis
- [ ] CI/CD Pipeline
- [ ] Kubernetes deployment
- [ ] Monitoramento com Prometheus/Grafana
- [ ] Testes unitários e integração

## 👥 Contribuindo

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/NovaFuncionalidade`)
3. Commit suas mudanças (`git commit -m 'feat: Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/NovaFuncionalidade`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## 📧 Contato

**Hackathon ONE 8 - Alura**

- GitHub: [@Araken13](https://github.com/Araken13)
- Projeto Original Python: [HACKATHON-ONE-8-ALURA](https://github.com/Araken13/HACKATHON-ONE-8-ALURA)

---

⭐ **Se este projeto foi útil, deixe uma estrela!** ⭐
