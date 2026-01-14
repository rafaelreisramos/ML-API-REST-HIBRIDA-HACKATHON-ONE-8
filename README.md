# 🔮 ChurnInsight: Inteligência Preditiva de Cancelamento

> **Plataforma Híbrida (Java + Python + React) para detecção de risco de Churn em tempo real.**
>
> *Versão Final v1.0 (Hackathon Alura G8)*

![Status](https://img.shields.io/badge/Status-Production_Ready-green)
![Docker](https://img.shields.io/badge/Docker-Zero_Config-blue)
![AI](https://img.shields.io/badge/AI_Model-RandomForest_G8-purple)
![Java](https://img.shields.io/badge/Backend-Java_Spring-orange)
![React](https://img.shields.io/badge/Frontend-React_Vite-cyan)

---

## 🏗️ Arquitetura do Projeto

O sistema opera sobre uma arquitetura de microserviços otimizada para deployment rápido e resiliência:

```mermaid
graph TD
    User[Usuário] -->|Acessa via HTTP| Frontend[Frontend React (Porta 80)]
    Frontend -->|GraphQL Query| Backend[Backend Java API (Porta 9999)]
    Backend -->|REST POST /predict| AIService[AI Service Python (Porta 5000)]
    
    subgraph "AI Core (Python)"
    AIService -->|Carrega| Model[RandomForest Model G8]
    AIService -->|Feature Engineering| Preproc[Processing.py]
    AIService -->|Auto-Healing| Rebuild[Rebuild Logic]
    end
    
    subgraph "Backend Core (Java)"
    Backend -->|Lê/Escreve| H2[H2 Database (Arquivo Local)]
    Backend -->|Autenticação| Security[Spring Security JWT]
    end
```

---

## 🚀 Como Rodar (Zero Config)

### Pré-requisitos

* **Docker** e **Docker Compose** instalados.

### Passo 1: Clonar e Iniciar

Este projeto é "Battery Included". O comando abaixo sobe Backend, Frontend e AI Service, além de configurar o banco de dados.

```bash
git clone https://github.com/Araken13/ML-API-REST-HIBRIDA-HACKATHON-ONE-8.git
cd ML-API-REST-HIBRIDA-HACKATHON-ONE-8

# Iniciar todo o stack
docker-compose up --build
```

*Aguarde alguns minutos. O Backend Java demora um pouco para inicializar completamente.*

### Passo 2: Acessar o Sistema

* **Dashboard (UI):** [http://localhost:80](http://localhost:80) (ou porta 3000 se 80 estiver ocupada)
* **GraphQL API:** [http://localhost:9999/graphiql](http://localhost:9999/graphiql)
* **AI Documentation:** [http://localhost:5000/docs](http://localhost:5000/docs)

**🔐 Credenciais Padrão:**

* **Login:** `admin`
* **Senha:** `123`

---

## 🧠 Inteligência Artificial (Modelo G8)

O sistema utiliza um modelo **RandomForest** customizado para prever o cancelamento de assinatura:

1. **Features Híbridas:** O sistema aceita dados brutos (CamelCase) e os normaliza automaticamente para o formato de treino (SnakeCase), aplicando feature engineering e RFE (Recursive Feature Elimination).
2. **Definição de Risco:**
   * **🔴 Alto Risco:** Probabilidade > **42.87%** (Threshold Otimizado).
   * **🟠 Risco Médio:** Probabilidade entre **25%** e **42.87%**.
   * **🟢 Baixo Risco:** Probabilidade < **25%**.
3. **Auto-Healing:** O container `ai-service` é capaz de reconstruir o modelo binário (`.joblib`) a partir dos dados de treino originais (`X_train.csv`) caso o arquivo do modelo seja corrompido ou perdido.

---

## 🛠️ Stack Tecnológico

| Camada | Tecnologia | Destaques |
|--------|------------|-----------|
| **Frontend** | React, Vite | Dashboard responsivo, Grid Layout 6-col, TailwindCSS + StyledComponents. |
| **Backend** | Java 17, Spring Boot 3 | API GraphQL, Spring Security, H2 Database, RestTemplate. |
| **AI Service** | Python 3.11, FastAPI | Scikit-learn 1.7.1, Pandas, Joblib. Serialização robusta. |
| **DevOps** | Docker Compose | Multi-stage builds, redes isoladas, volumes persistentes. |

---

## 📂 Estrutura de Diretórios

```
/
├── ai_service/          # Microserviço Python (FastAPI + Modelos + Treinamento)
├── src/                 # Código Fonte Java (Spring Boot Backend)
├── frontend/            # Aplicação React (Vite)
├── hackathon_g8_one/    # Artefatos Originais de Data Science
├── docker-compose.yml   # Definição dos Serviços
└── Dockerfile.backend   # Descritor de Build Java
```

---

## 🧪 Testes e Validação

Para validar a integridade do sistema, incluímos scripts de teste:

```bash
# Teste de Ponta-a-Ponta (E2E)
./scripts/run_e2e_tests.sh
```

---

**Desenvolvido por:** Equipe G8 Hackathon Alura
