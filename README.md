# 🔮 ChurnInsight: Inteligência Preditiva de Cancelamento (Zero Config & OCI Ready)

> **Plataforma Híbrida de ML + Fullstack para detecção de risco de Churn em tempo real.**
>
> *Versão Final v1.0 (Hackathon Edition)*

![Status](https://img.shields.io/badge/Status-Production_Ready-green)
![OCI](https://img.shields.io/badge/Cloud-Oracle_OCI-orange)
![Docker](https://img.shields.io/badge/Docker-Zero_Config-blue)
![AI](https://img.shields.io/badge/AI_Model-RandomForest_G8-purple)

---

## 🚀 Sobre o Projeto

O **ChurnInsight** é uma solução completa que integra um modelo de **Machine Learning (Python)** com um backend corporativo (**Java Spring Boot**) e uma interface moderna (**React**), projetada para identificar clientes com alto risco de cancelamento.

### 🌟 Destaques da Arquitetura

* **Zero Configuração:** Basta ter Docker instalado. O banco de dados (H2) é embutido e o ambiente é auto-configurável.
* **OCI Always Free Compatible:** Infraestrutura Terraform pronta para rodar sem custos na nuvem Oracle.
* **Modelo Real Integrado:** Modelo RandomForest (29MB) treinado com dados reais/sintéticos do Hackathon, capaz de detectar padrões complexos.
* **Auto-Healing AI:** O serviço de inteligência artificial detecta corrupção de modelo e se auto-repara/treina em tempo de execução se necessário.

---

## 🛠️ Tecnologias

* **Backend:** Java 17, Spring Boot 3, GraphQL, JPA, H2 Database (In-Memory/File).
* **AI Service:** Python 3.11, FastAPI, Scikit-learn 1.7.1, Pandas, Joblib.
* **Frontend:** React, Vite, Nginx, TailwindCSS/StyledComponents.
* **DevOps:** Docker Compose (Multi-stage), Terraform (OCI), GitHub Actions.

---

## ⚡ Quick Start (Rodando Localmente)

### Pré-requisitos

* **Docker** e **Docker Compose** instalados (apenas isso!).

### 1. Clonar e Rodar

```bash
git clone https://github.com/SEU_USUARIO/churn-insight.git
cd churn-insight

# Build e execução de TODO o stack (Backend + Frontend + AI)
docker-compose up --build
```

### 2. Acessar

* **Frontend (UI):** [http://localhost:80](http://localhost:80) (ou <http://localhost:3000>)
  * *Login:* `admin` / `123`
* **API GraphQL:** [http://localhost:9999/graphiql](http://localhost:9999/graphiql)
* **AI Docs:** [http://localhost:5000/docs](http://localhost:5000/docs)

---

---

## 🐧 Suporte a WSL 2 / Linux

Se você estiver usando Windows com **WSL 2**, criamos scripts para facilitar sua vida e resolver erros comuns de permissão e credenciais do Docker Desktop:

```bash
# Corrige erro "exec format error / docker-credential-desktop.exe"
./scripts/fix_wsl_docker.sh

# Roda os testes E2E ignorando bloqueios de Firewall do Windows
./scripts/run_e2e_tests.sh
```

👉 *Para mais detalhes sobre problemas e soluções, veja o [Manual de Erros](MANUAL_DE_ERROS.md).*

---

## ☁️ Deploy na Oracle Cloud (OCI)

Este projeto inclui um pipeline completo de **Infrastructure as Code (IaC)** para a Oracle Cloud, otimizado para o **Always Free Tier**.

👉 **[Consulte o Guia de Deploy OCI Completo](oci-pipeline/DEPLOY_GUIDE.md)**

* **Custo Estimado:** R$ 0,00/mês.
* **Recursos:** 2x VMs (Compute E2.1.Micro), VCN, Security Lists, Public IPs.

---

## 🧪 Testes e Validação

Para validar a integridade do sistema, incluímos scripts de teste E2E:

```bash
# Opção 1: Via Script (Recomendado para WSL/Docker)
./scripts/run_e2e_tests.sh

# Opção 2: Localmente (Requer Python instalado)
pip install requests pandas

# Teste de Integração (Frontend -> Java -> Python)
python test_api_e2e.py

# Teste de Processamento em Lote (Performance)
python test_optimized_batch.py
```

---

## 📂 Estrutura do Projeto

```
/
├── ai_service/          # Microserviço Python (FastAPI + Modelos)
├── src/                 # Backend Java Spring Boot
├── frontend/            # Aplicação React SPA
├── hackathon_g8_one/    # Artefatos de Data Science (Modelos, CSVs)
├── oci-pipeline/        # Terraform e Documentação de Cloud
├── docker-compose.yml   # Orquestração local
└── Dockerfile.backend   # Descritor de build do Java
```

---

## 📚 Documentação Adicional

* [Guia de Deploy OCI](oci-pipeline/DEPLOY_GUIDE.md)
* [Limites do Free Tier](oci-pipeline/FREE_TIER_LIMITS.md)
* [Manual Jupyter (Demos)](MANUAL_JUPYTER.md)
* [Guia de Segurança](SECURITY_GUIDE.md)
* [Changelog](CHANGELOG.md)

---

**Equipe:** G8 Hackathon Alura + Google Gemini (Antigravity Agent)
