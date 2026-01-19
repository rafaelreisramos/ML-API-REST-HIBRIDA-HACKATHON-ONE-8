# 🧪 Relatório Científico: Prevenção de Churn Streaming

![Dataset](https://cdn.telaviva.com.br/wp-content/uploads/2021/04/Cancel-e1688593083761.jpeg)

## 🗺️ Visão Geral

Este documento detalha o trabalho do time de **Data Science** no desenvolvimento do motor preditivo para a plataforma de streaming. O foco foi transformar dados brutos de sistemas legados em inteligência acionável.

---

## 📅 Links e Recursos

- [Notebook Criação Dataset](./Dataset_Churn_Streaming_Hackathon.ipynb)
- [Dataset (Fonte)](https://raw.githubusercontent.com/rafaelreisramos/oracle-one-g8-hackathon/refs/heads/main/data/dados_streamingV4.csv)
- [Notebook EDA](./EDA_Streaming.ipynb)
- [Notebook Modelo Final](./Streaming_DS.ipynb)

---

## 1. Problema de Negócio

O objetivo principal foi identificar por que a taxa de cancelamento disparou nos últimos meses. Analisamos 30.000 clientes integrando dados de CRM, Billing e Analytics.

**Público-alvo:** Serviços de Streaming.

---

## 2. Dicionário de Dados Resumido

| Variável | Descrição |
| :--- | :--- |
| **churn** | **TARGET**: 1 para cancelado, 0 para ativo. |
| **idade** | Idade do cliente. |
| **dias_ultimo_acesso** | Dias desde a última sessão. |
| **visualizacoes_mes** | Total de conteúdo assistido no mês. |
| **contatos_suporte** | Quantidade de chamados abertos. |

---

## 3. Metodologia: O Ciclo da Inteligência

Utilizamos o ecossistema Python moderno:

- **Limpeza:** Tratamento de nulos via MNAR (Missing Not At Random) para preservar o valor preditivo do "descontentamento silencioso".
- **EDA:** Descoberta de que o *Gênero* e *Idade* não são drivers, mas o *Engajamento* sim.
- **Engenharia de Features:** Criação de scores de engajamento acumulado.

---

## 4. Limpeza e Tratamento de Dados

Encontramos lacunas significativas em avaliações de conteúdo. Adotamos a estratégia de preencher como **"Nao_preenchido"** em vez de médias, pois a ausência de avaliação é um dado por si só (indiferença ou satisfação extrema).

---

## 5. Principais Descobertas (Insights)

- **O Abismo do Suporte:** Clientes com 3+ contatos têm **46,4% de churn**.
- **O Poder do Recorrente:** Pagamentos via Boleto têm **47,2% de churn** contra apenas 18,6% do Crédito Recorrente.
- **Janela de Inatividade:** Inatividade acima de 60 dias eleva o risco para **81,7%**.

---

## 6. Performance do Modelo

O modelo **Random Forest** final foi calibrado para ser extremamente rigoroso:

- **F1-Score:** 0.9531
- **ROC-AUC:** 0.9957
- **Drivers de Peso:** Engajamento (29%) e Tempo de Sessão (26%) dominam a predição.

![Feature Importance](https://github.com/JeanKahlilR/Hackathon-One/blob/main/feature_importance.png?raw=true)

---
*Relatório gerado pelo Time de Data Science - G8*
