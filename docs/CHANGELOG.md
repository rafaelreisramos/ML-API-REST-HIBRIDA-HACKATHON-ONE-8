# Histórico de Mudanças (Changelog)

## [2026-01-18] - Documentação e Organização do Projeto

Reorganização completa da estrutura de arquivos e finalização da documentação.

### 🧪 Testes Locais

* **`developer_tools/scripts/presentation_cover_local.ps1`**: Novo script para rodar a demo de apresentação localmente, utilizando um orquestrador dedicado (`orquestrador_local.py`).
* **`developer_tools/scripts/run_tests_local.bat`**: Script batch dedicado para execução da suíte de testes em ambiente local (`localhost`).
* **`developer_tools/scripts/local_test_graphql.py`**: Novo teste de conectividade GraphQL específico para validação local, sem dependência da OCI.
* **Isolamento de Ambiente**: Scripts ajustados para garantir que testes locais não tentem conectar acidentalmente na infraestrutura OCI.

### 📚 Documentação

* **Pasta `/docs`**: Centralização de todos os arquivos de documentação (13 arquivos .md).
* **Pasta `/docs/csv`**: Organização dos arquivos CSV de teste e resultados.
* **README Atualizado**: Mapa completo da documentação com links funcionais.
* **Manual de Uso**: Atualizado com senha correta (123456) e fluxo de criação de usuários.

### 🛠️ Scripts e Ferramentas

* **Pasta `/developer_tools/scripts`**: Consolidação de 21 scripts (Python, PowerShell, Bash).
* **Testes E2E**: Movidos para pasta centralizada.
* **Scripts de Deploy**: Organizados junto com demais ferramentas.

### 🔧 Correções

* **Diagramas Mermaid**: Corrigidos erros de parse em `OCI_NETWORK_DOCS.md` e `PROJECT_ARCHITECTURE_WORKFLOW.md`.
* **Links Quebrados**: Todos os links internos atualizados após reorganização.

---

## [2026-01-17] - Deploy OCI Enterprise

Deploy da infraestrutura completa na Oracle Cloud com VMs Intel Flex.

### ☁️ Infraestrutura OCI

* **App Server**: VM.Standard3.Flex (2 vCPUs, 8GB RAM) - IP: 137.131.179.58
* **AI Server**: VM.Standard3.Flex (4 vCPUs, 16GB RAM) - IP: 163.176.245.6
* **Cloud-Init**: Configuração automática de Docker e aplicação.

### 🔐 HTTPS Automático

* **Traefik**: Configurado como reverse proxy com SSL/TLS.
* **Let's Encrypt**: Certificados automáticos via nip.io.
* **Docs**: Criado `HTTPS_CONFIGURATION.md` com guia completo.

---

## [2026-01-13] - Zero Config & OCI Production Ready

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
