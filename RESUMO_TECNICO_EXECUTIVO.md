# 📘 Resumo Técnico & Manual de Decisões do Projeto

**Este documento serve como um guia explicativo detalhado sobre as escolhas arquiteturais, as correções realizadas e o funcionamento do sistema, destinado a gestores e analistas de software.**

---

## 1. 🏗️ Reconstrução & Integridade do Projeto

### O que foi feito?

Utilizamos uma ferramenta personalizada (`construtor_projeto.py`) para "hidratar" o projeto a partir de um arquivo de contexto único (`PROJECT_CONTEXT_PDR.txt`).

### Por que isso foi necessário?

* **Portabilidade Extrema:** Em vez de lidar com centenas de arquivos soltos ou depender de clones de repositórios que podem estar desatualizados, centralizamos a "verdade" do projeto em um único arquivo de texto auditável.
* **Segurança anti-alucinação:** Garante que a IA (e o desenvolvedor) estejam trabalhando extamente na versão que possui as definições mais recentes, sem "ruído" de arquivos antigos.

---

## 2. 🔧 Correções Críticas de Infraestrutura (Docker & AI)

Durante a inicialização, encontramos e corrigimos um bloqueio crítico no serviço de Inteligência Artificial.

### O Problema

O serviço de IA falhou ao iniciar porque as bibliotecas modernas de aprendizado de máquina (`scikit-learn` recente) exigem uma versão mais nova da linguagem Python (3.11+), mas o projeto estava configurado para uma versão antiga (3.10).

### A Solução e Justificativa

1. **Atualização do Dockerfile:** Alteramos a imagem base de `python:3.10-slim` para `python:3.11-slim`.
    * *Necessidade:* Compatibilidade obrigatória com as bibliotecas de Data Science atuais.
2. **Flexibilização de Requisitos:** Removemos a trava de versão rígida (`==1.8.0`) do `scikit-learn` no arquivo `requirements.txt`.
    * *Necessidade:* Evitar que o projeto quebre no futuro por buscar uma versão específica que pode se tornar obsoleta ou incompatível com o sistema operacional. Deixamos o instalador escolher a melhor versão compatível.

---

## 3. 🏛️ Arquitetura Híbrida: Por que essas escolhas?

O sistema não é monolítico; ele é composto por três peças fundamentais que conversam entre si. Entenda o porquê de cada uma:

### A. O "Cérebro" (AI Service - Python)

* **Tecnologia:** Python + FastAPI + Scikit-Learn.
* **Por que?** Python é a lingua franca da ciência de dados. Tentar fazer IA avançada em Java ou Javascript seria ineficiente e complexo. Isolamos isso em um "container" separado para que ele possa escalar ou ser atualizado sem derrubar o resto do site.

### B. A "Espinha Dorsal" (Backend - Spring Boot / Java)

* **Tecnologia:** Java 17 + Spring Boot + GraphQL + MongoDB.
* **Por que?**
  * **Java/Spring:** Robustez corporativa. Aguenta alta carga e é seguro.
  * **GraphQL:** Diferente de APIs antigas (REST), permite que o Front-end peça *apenas* os dados que precisa. Isso economiza banda e deixa o site mais rápido.
  * **MongoDB:** Um banco de dados que não exige tabelas fixas (como Excel). Perfeito para dados variáveis de clientes e resultados de IA, que podem mudar de formato.

### C. A "Face" (Frontend - React)

* **Tecnologia:** React + Vite.
* **Por que?** Oferece uma experiência de usuário fluida, parecida com um aplicativo de celular, sem precisar recarregar a página a cada clique.

---

## 4. 🔄 Fluxo de Operação (Como tudo se conecta)

1. **O Usuário** acessa o site (Frontend - Porta 5173).
2. Ele envia um arquivo de dados de clientes para análise.
3. O **Frontend** passa isso para o **Backend** (Porta 9999).
4. O **Backend** salva os dados no **MongoDB** e chama o **AI Service** (Porta 5000).
5. O **AI Service** processa a matemática pesada e devolve a previsão de Churn (rotatividade).
6. O resultado volta todo o caminho até aparecer na tela do usuário.

---

## 5. ✅ Estado Atual

O sistema está **100% Operacional** e rodando localmente ("End-to-End").

* Todas as portas de comunicação foram testadas.
* O ambiente está "Dockernizado" (isolado em containers), o que significa que funcionará igual na máquina de qualquer outro desenvolvedor.
