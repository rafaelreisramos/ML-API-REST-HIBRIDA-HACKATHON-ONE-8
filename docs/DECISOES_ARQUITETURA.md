# 🏛️ Decisões de Arquitetura e Justificativas (Architecture Decisions)

Este documento detalha o racional por trás das escolhas tecnológicas do projeto **ChurnInsight**, explicando as vantagens estratégicas e técnicas de cada decisão.

---

## 1. Abordagem Híbrida: RESTful & GraphQL

### 🎯 A Decisão

Implementar ambos os protocolos de API simultaneamente na mesma aplicação, em vez de escolher apenas um.

### 💡 Por que escolhemos assim?

* **Eficiência no Frontend (GraphQL):** O dashboard administrativo precisa exibir listas complexas. Com GraphQL, o frontend pede apenas os campos necessários (ex: `clienteId` e `previsao`), evitando o *over-fetching* (baixar dados inúteis como endereço ou histórico completo apenas para mostrar uma tabela simples). Isso economiza banda e memória.
* **Compatibilidade Universal (REST):** Nem todos os sistemas sabem falar GraphQL. Manter endpoints REST (`POST /predict`, `POST /batch`) garante que sistemas legados, scripts simples (curl/bash) e webhooks de terceiros possam se integrar facilmente.

> **Vantagem:** O melhor dos dois mundos: flexibilidade para desenvolvedores Frontend e simplicidade para integrações Backend-to-Backend.

---

## 2. Microserviços Poliglotas: Java + Python

### 🎯 A Decisão

Utilizar **Java (Spring Boot)** para o Core da aplicação e **Python (FastAPI)** exclusivamente para o Serviço de IA.

### 💡 Por que escolhemos assim?

* **O Melhor de Cada Ecossistema:**
  * **Java**: É o padrão da indústria para aplicações corporativas robustas. Oferece tipagem estática, gerenciamento de memória maduro e frameworks de segurança (Spring Security) inigualáveis.
  * **Python**: É a língua nativa da Ciência de Dados. Tentar rodar modelos de ML em Java (via DL4J ou pontes) é complexo e limita o uso das bibliotecas mais modernas (Scikit-Learn, Pandas).
* **Escalabilidade Independente:** Modelos de IA consomem muita CPU. Regras de negócio consomem Memória/IO. Ao separá-los em containers diferentes, podemos escalar o `ai-service` (ex: 5 réplicas) enquanto mantemos apenas 1 réplica do `backend`, otimizando recursos de infraestrutura (Kubernetes/AWS).

> **Vantagem:** Arquitetura desacoplada onde cada linguagem faz o que faz de melhor.

---

## 3. Persistência Dual: Pattern "Double-Write"

### 🎯 A Decisão

Gravar os dados simultaneamente em um banco em memória (**H2**) e em um banco relacional robusto (**PostgreSQL**).

### 💡 Por que escolhemos assim?

* **Zero Latência (H2):** Para a hackathon e demos, a velocidade é crucial. O H2 roda na memória RAM da JVM. Consultas de dashboards complexos respondem em microssegundos.
* **Segurança e Durabilidade (PostgreSQL):** Dados em memória são voláteis. O Postgres atua como "Cold Storage". Se o container reiniciar, os dados estão salvos no disco.
* **Resiliência (Fail-Over):** Devido à implementação com `try-catch` isolado e clonagem de objetos, se o banco PostgreSQL ficar indisponível, a aplicação **não para**. Ela continua operando apenas com o H2, garantindo alta disponibilidade (embora sem persistência durável momentânea).

> **Vantagem:** Velocidade extrema de desenvolvimento/uso sem sacrificar a segurança dos dados a longo prazo.

---

## 4. Estratégia de Batch Processing (Paralelismo)

### 🎯 A Decisão

Utilizar `CompletableFuture` e `ExecutorService` com pool de threads fixo (20 threads) para processamento de CSVs.

### 💡 Por que escolhemos assim?

* **O Gargalo:** Processar previsão de Churn item a item para um arquivo de 50.000 clientes demoraria horas em uma thread única (bloqueio de I/O na chamada HTTP e no Banco).
* **A Solução:** Dividir o trabalho. Enquanto uma thread espera a resposta da IA, outra está salvando no banco e outra está lendo do arquivo.
* **Bulk Insert:** Em vez de fazer 1000 `INSERT`s no banco, acumulamos os resultados e fazemos 1 `INSERT` de 1000 registros. Isso reduz drasticamente o overhead de transação do banco de dados.

> **Vantagem:** Capacidade de processar grandes volumes de dados (Big Data ready) em tempo aceitável para o usuário.

---

## 🏆 Conclusão

A arquitetura do **ChurnInsight** não foi uma escolha aleatória, mas sim um desenho deliberado para atender requisitos de **Performance**, **Usabilidade** e **Robustez**. Ela demonstra maturidade técnica ao resolver problemas complexos (como conflitos de identidade JPA em escritas duplas e gargalos de I/O) com soluções elegantes e padronizadas.
