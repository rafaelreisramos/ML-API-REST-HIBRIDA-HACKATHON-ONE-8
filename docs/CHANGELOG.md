# Histórico de Mudanças (Changelog)

## [2026-01-13] - Zero Config & OCI Production Ready

Finalização do projeto com foco em "Zero Configuration" para execução local e preparação total para deploy em nuvem (OCI).

### 🚀 Infraestrutura & Cloud (OCI)

* **OCI Pipeline:** Criada infraestrutura completa como código (Terraform) para **Oracle Cloud Always Free Tier**.
* **Zero Cost:** Arquitetura otimizada para R$ 0,00/mês (2x VMs E2.1.Micro).
* **CI/CD:** Pipeline GitHub Actions para build e deploy automático.

### 🐳 Docker Profissional

* **Self-Contained:** Dockerfiles refatorados (Multi-stage build) que eliminam dependências externas.
* **Otimização:** Build do AI Service inclui modelo real (29MB) e dependências (`scikit-learn==1.7.1`).
* **Cleanup:** Remoção de 3.5GB de arquivos temporários e scripts de debug.

### 🧠 Integração AI Definitiva

* **Modelo Real:** Substituição do placeholder (79 bytes) pelo modelo treinado real (29MB).
* **Correção de Dependências:** Sincronização de versões (`scikit-learn` atualizado) para eliminar warnings.
* **Auto-Healing:** Mecanismo mantido como fallback de segurança.
* **Testes:** Validação completa (Java Backend + AI Service + Batch Processing).

### 💾 Banco de Dados

* **H2 Database:** Migração completa de MongoDB para H2 (In-Memory/File), eliminando necessidade de instalação de banco local.

## [2026-01-12] - Integração do Modelo V8 + E2E Cirúrgico

Integração completa do modelo de machine learning `hackathon_g8_one` (V8) com pipeline de pré-processamento avançado.

### 🤖 AI Service (Python)

* **Modelo V8:** Implantação de `modelo_churn.joblib` com 100 árvores (Random Forest).
* **Pipeline RFE:** Seleção automática de features e cálculo de variáveis derivadas (`engajamento_score`, `risco_score`).
* **Estabilidade:** Fallback inteligente para Mock Model em caso de incompatibilidade de versão.

### ☕ Backend API (Java/GraphQL)

* **Novos Campos:** Adicionados `tipoContrato`, `categoriaFavorita` e `acessibilidade` ao Schema e Entidade.
* **Validação:** Schema GraphQL sincronizado com requisitos do novo modelo.

### ✅ Testes & DevOps

* **E2E:** Teste end-to-end `test_api_e2e.py` atualizado para validar fluxo completo com novo payload.
* **Infra:** Dockerfile otimizado para incluir artefatos de IA.
* **Batch Processing:** Correção no parser CSV (`ChurnBatchService`) para processar novos campos e garantir previsões em lote.
* **Auto-Healing:** AI Service retreina o modelo automaticamente em tempo de execução se o binário estiver corrompido.

## [2026-01-12] - Automação e Demonstração via Jupyter

Adicionada camada de orquestração via Notebooks para facilitar apresentações e execução "One-Click".

### ✨ Novas Funcionalidades

* **Notebooks:** `Controlador_Do_Projeto.ipynb` (infra/execução) e `Demo_Interativa_API.ipynb` (cliente).
* **Documentação:** `GUIA_RAPIDO_APRESENTACAO.md` e `MANUAL_JUPYTER.md` adicionados.

## [2026-01-11] - Consolidação e Revisão Hackathon

Revisão completa do código e ajustes na infraestrutura.

### � Melhorias e Segurança

* **Docker:** Correção JWT e portas no `docker-compose.yml`.
* **E2E:** Fix payload GraphQL e validação de campos obrigatórios.
* **Segurança:** `TokenService` validado e ativo.

### 🐛 Fixes

* [x] Cadastro e Login funcionais.

* [x] Erro 'Secret cannot be null' corrigido.
* [x] Fluxo de Mutation Seguro validado.
