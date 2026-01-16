# 📊 ChurnInsight: Monitoramento de Risco de Cancelamento

> **Sistema Híbrido de Inteligência Artificial para Previsão de Churn**
> *Hackathon Alura G8 - Solução Enterprise*

![Status](https://img.shields.io/badge/Status-Stable-green)
![Docker](https://img.shields.io/badge/Docker-Zero_Config-blue)
![Stack](https://img.shields.io/badge/Stack-Java_Python_React-orange)
![License](https://img.shields.io/badge/License-MIT-purple)

---

## 🧐 O que é este projeto?

O **ChurnInsight** é uma plataforma analítica completa que ajuda empresas a identificar quais clientes têm maior probabilidade de cancelar seus serviços (Churn).

Diferente de soluções simples, este sistema é **Full-Stack e Híbrido**:

* **IA Real**: Usa um modelo *RandomForest* treinado em Python.
* **API Híbrida**: Oferece **REST** (para integração legada) e **GraphQL** (para frontends modernos).
* **Dashboard Interativo**: Interface React para análise em tempo real.
* **Processamento Massivo**: Pipeline otimizado para processar arquivos CSV com 50.000+ clientes em minutos.

---

## 📚 Documentação Completa

Para detalhes específicos, consulte nossos guias oficiais incluídos neste repositório:

| Documento | Descrição |
| :--- | :--- |
| [📘 Manual de Uso](./MANUAL_DE_USO.md) | Guia para o usuário final: como navegar, interpretar gráficos e usar o simulador. |
| [📡 Documentação da API](./API_DOCUMENTATION.md) | Swagger, Endpoints, Schemas GraphQL e exemplos de cURL. |
| [🏛️ Decisões de Arquitetura](./DECISOES_ARQUITETURA.md) | Por que usamos Java + Python? Por que 2 bancos de dados? Leia aqui. |

---

## 🚀 Guia Rápido (Quick Start)

Rodar este projeto é extremante simples. Você precisa apenas do **Docker Desktop** instalado.

### 1. Clonar o Repositório

```bash
git clone https://github.com/Araken13/ML-API-REST-HIBRIDA-HACKATHON-ONE-8.git
cd ML-API-REST-HIBRIDA-HACKATHON-ONE-8
```

### 2. Iniciar o Ambiente

No terminal, dentro da pasta do projeto:

```bash
docker-compose up -d --build
```

> *Aguarde cerca de 2 minutos na primeira vez para o build dos containers e inicialização do Banco de Dados.*

### 2. Acessar o Sistema

* **Frontend (Dashboard):** [http://localhost:3000](http://localhost:3000)
* **Login:** `admin`
* **Senha:** `123`

### 3. Links de Desenvolvimento

* **GraphQL Playground:** [http://localhost:9999/graphiql](http://localhost:9999/graphiql)
* **Swagger UI (AI Service):** [http://localhost:5000/docs](http://localhost:5000/docs)

---

## 🆘 Troubleshooting (Problemas Comuns)

**🔴 Erro: `Conflict. The container name "/ai-service" is already in use`**
Isso acontece se você rodou o projeto antes e ele não desligou corretamente.

* **Solução:** Rode este comando para limpar containers antigos:

    ```bash
    docker rm -f $(docker ps -aq)
    ```

**🔴 Erro: Frontend não carrega os dados**
Certifique-se de que o Backend (Porta 9999) subiu completamente.

* **Solução:** Verifique os logs:

    ```bash
    docker logs backend-api -f
    ```

---

## 🏗️ Arquitetura do Sistema

Operamos com 3 serviços principais orquestrados:

```mermaid
graph TD
    User["Usuário / Analista"] -->|Navegador| UI["Frontend React (Porta 3000)"]
    UI -->|"GraphQL / REST"| API["Backend Java (Porta 9999)"]
    API -->|"Predição (HTTP)"| AI["AI Service Python (Porta 5000)"]
    
    subgraph "Persistência"
    API -->|"Rápido"| H2["H2 (Memória)"]
    API -->|" Seguro"| PG["PostgreSQL (Disco)"]
    end
```

### Destaques Técnicos

* **Auto-Healing**: Se o serviço de IA cair, ele reinicia automaticamente.
* **Double-Write**: Gravamos dados no H2 (para velocidade extrema no dashboard) e no PostgreSQL (para segurança) simultaneamente.
* **Poliglota**: Backend em Java (Spring Boot 3) e IA em Python (FastAPI + Scikit-Learn).

---

## 🧪 Testes Automatizados

O projeto inclui scripts que testam o fluxo de ponta a ponta (Login -> Upload -> Previsão).

**Executar todos os testes (Windows Powershell):**

```powershell
./run_all_tests.ps1
```

---

**Desenvolvido pela Equipe G8**
