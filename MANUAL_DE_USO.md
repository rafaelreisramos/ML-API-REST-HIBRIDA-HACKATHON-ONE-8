# 📘 Manual de Uso - ChurnInsight

Este manual descreve como operar a plataforma **ChurnInsight**, desde a navegação na interface até a interpretação das predições de IA.

---

## 1. Acesso ao Sistema

Após iniciar o sistema (via Docker ou local), acesse no navegador:

* **URL:** `http://localhost:3000` (ou porta 80 via Docker)
* **Login Padrão:**
  * **Usuário:** `admin` (ou `test_admin_v4`)
  * **Senha:** `123`

---

## 2. Funcionalidades Principais

### 🏠 Dashboard Principal

* **Visão Geral:** Métricas consolidadas de clientes analisados, taxa de alto risco e churn rate médio.
* **Feed em Tempo Real:** Lista lateral mostrando as últimas análises processadas pelo sistema, com indicadores visuais de risco (Verde = Baixo, Vermelho = Alto).

### 🔍 Simulador Individual (Real-Time)

Use esta aba para analisar um cliente específico.

1. Preencha os campos do formulário (Idade, Gênero, Plano, Consumo, etc.).
2. Clique em **"Analisar Risco de Churn"**.
3. O sistema processará os dados em tempo real usando o modelo **RandomForest G8**.
4. O resultado exibirá:
    * **Probabilidade:** % de chance de cancelamento.
    * **Classificação:** "Vai continuar" ou "Vai cancelar".
    * **Explicação:** Fatores principais (se disponível).

### 📦 Processamento Batch (Massivo)

Use esta aba para processar arquivos CSV com milhares de clientes.

1. Prepare um arquivo CSV seguindo o modelo (colunas: `idade`, `plano`, `tempo_assinatura`, etc.).
2. Arraste o arquivo para a área de upload.
3. Clique em **"Processar Arquivo"**.
4. O sistema processará assincronamente (aprox. 5.000 registros/segundo).
5. Baixe o relatório final com as previsões adicionadas.

---

## 3. Entendendo a Inteligência Artificial

O sistema utiliza um modelo **RandomForest** treinado em dados de telecom/streaming.

* **Campos Críticos:**
  * *Dias desde último acesso:* Forte indicador de inatividade.
  * *Avaliação de Conteúdo:* Notas baixas aumentam drasticamente o risco.
  * *Tempo de Sessão:* Sessões curtas indicam desengajamento.
* **Threshold (Limiar):** O modelo decide o churn com base em um limiar otimizado (aprox. 0.42). Probabilidades acima disso são marcadas como Risco.

---

## 4. Solução de Problemas (FAQ)

**Q: O sistema diz "Serviço de IA Indisponível/Offline".**

* **Causa:** O container `ai-service` pode estar parado ou reiniciando.
* **Ação:** Verifique os logs (`docker logs ai-service`). O sistema possui *Auto-Healing*, aguarde 30 segundos e tente novamente.

**Q: Minha previsão deu 0% ou 100% cravado.**

* **Causa:** Pode ser um mock de emergência se o modelo real falhou, ou um caso extremo muito claro.
* **Ação:** Verifique no feed se aparece "RandomForest G8". Se aparecer "MockModel", o sistema está usando a contingência. Reinicie o container para tentar recarregar o modelo real.

**Q: Onde estão os dados salvos?**

* **H2 Database:** Os dados são persistidos em arquivos locais na pasta `./data` ou na memória do container, dependendo do perfil de execução.

---

**Suporte:** Entre em contato com a equipe de Data Science (G8).
