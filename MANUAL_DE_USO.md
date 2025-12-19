# 📘 Manual de Uso - ChurnInsight 2.0

Bem-vindo ao manual de operação do sistema ChurnInsight. Este documento guia você por todas as funcionalidades disponíveis na plataforma.

---

## 🚀 Funcionalidades Principais

### 1. Dashboard em Tempo Real

Ao abrir o sistema, você é recebido com indicadores chave de performance (KPIs):

* **Total Analisado:** Número de clientes visíveis no sistema.
* **Risco Previsto:** Quantidade de clientes que a IA identificou como "Alto Risco de Churn".
* **Taxa de Churn:** Porcentagem da base comprometida.

### 2. Simulador Individual ("Simular Impacto")

Permite testar cenários hipotéticos ("O que aconteceria se...?").

1. Preencha o formulário com dados do cliente (idade, uso, satisfação).
2. Clique em **"Simular Impacto"**.
3. **Resultado Instatâneo:** O sistema mostra se o cliente "Vai continuar" ou "Vai cancelar" e a probabilidade exata (ex: 85.5%).

### 3. Processamento em Lote (Batch Upload)

Ideal para analisar milhares de clientes de uma vez.

1. Na área "Processamento em Lote", clique para selecionar seu arquivo CSV.
2. O sistema processa o arquivo em background.
3. **Download Automático:** Um novo CSV ("resultado_...") será baixado com as colunas de previsão adicionadas.
4. O Dashboard é atualizado automaticamente com esses novos números.

---

## 🛡️ Funcionalidade de Arquivamento (Reset de Dashboard)

Uma nova funcionalidade foi adicionada para permitir "limpar a mesa" sem perder dados históricos.

### Como Funciona?

* No canto superior direito, existe um botão vermelho: **🗑️ Arquivar Dashboard**.
* Ao clicar, todos os dados visíveis atualmente são **arquivados**.
* O Dashboard voltará a mostrar **zeros**, pronto para uma nova rodada de análises.

### Segurança (Modo "Soft Delete")
 >
 > **Importante:** Nenhum dado é realmente apagado do banco de dados!

O sistema apenas marca os registros como "Inativos" e grava a data do arquivamento. Isso garante que:

1. Você tenha uma visão limpa para trabalhar.
2. A empresa mantenha o histórico completo para auditoria futura.
3. Evita acidentes catastróficos de perda de dados.

---

## 🆘 Solução de Problemas

* **Erro "Conexão Recusada":** Verifique se o Backend (Terminal Java) e o Frontend estao rodando.
* **CSV não processa:** Certifique-se de que o CSV usa ponto (.) para decimais, não vírgula.
* **Previsão "Erro":** O serviço de IA (Python) pode estar desligado. O sistema salvará os dados, mas sem previsão.

---
*Versão do Manual: 1.0 - Dezembro 2025*
