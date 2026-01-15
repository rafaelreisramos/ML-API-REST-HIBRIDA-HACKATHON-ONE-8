# 📘 Manual de Uso - ChurnInsight

Bem-vindo ao **ChurnInsight**, sua plataforma de inteligência artificial para previsão e retenção de clientes.

---

## 🔐 1. Acesso ao Sistema

O sistema é protegido por autenticação.

* **URL de Acesso:** [http://localhost:3000](http://localhost:3000) (ou porta 80)
* **Credenciais (Admin):**
  * **Usuário:** `admin`
  * **Senha:** `123`

> **Nota:** Se for o primeiro acesso, pode levar alguns segundos para carregar o dashboard enquanto os serviços "esquentam".

---

## 🖥️ 2. Navegando na Plataforma

### 🏠 Dashboard Principal

O painel de controle oferece uma visão macro da sua base de clientes.

* **Métricas Chave:** Total de clientes analisados, Percentual de risco, Churn Rate estimado.
* **Feed em Tempo Real:** Acompanhe análises chegando instante a instante. O sistema utiliza *WebSockets* para atualizar esta lista sem precisar recarregar a página.

### 🔍 Simulador Individual (Análise Unitária)

Ideal para atendentes de suporte ou gerentes de conta que desejam analisar a situação de um cliente específico.

**Como usar:**

1. Acesse a aba **"Simulador"**.
2. Preencha os dados cadastrais e comportamentais do cliente.
    * *Dica: Campos como "Dias desde o último acesso" e "Avaliação" têm alto impacto.*
3. Clique em **"Calcular Risco"**.
4. **Resultado:**
    * 🔴 **Alta Probabilidade (>42%):** Ação imediata recomendada (oferta de desconto, contato proativo).
    * 🟢 **Baixa Probabilidade:** Cliente saudável.

### 📦 Processamento Batch (Análise em Massa)

Ideal para analistas de dados que precisam processar bases inteiras (ex: 50.000 clientes) de uma só vez.

**Como usar:**

1. Acesse a aba **"Batch Upload"**.
2. Prepare seu arquivo CSV (veja o modelo abaixo).
3. Arraste o arquivo para a área pontilhada.
4. Acompanhe a barra de progresso.
5. Ao final, o download do arquivo processado (com a coluna `probabilidade_churn`) iniciará automaticamente.

#### 📝 Modelo de CSV Esperado

O arquivo deve conter cabeçalho e ser separado por vírgulas. Colunas essenciais:

```csv
clienteId,idade,genero,regiao,valorMensal,diasUltimoAcesso,avaliacaoPlataforma
C001,35,Masculino,Sudeste,59.90,2,4
C002,28,Feminino,Sul,29.90,45,1
...
```

> **Importante:** O sistema é robusto e tentará inferir valores ausentes, mas quanto mais completo o dado, mais precisa a previsão.

---

## 🧠 3. Entendendo a Inteligência Artificial

O "cérebro" do ChurnInsight é um modelo **RandomForest** treinado com dados históricos de cancelamentos.

### O que o modelo "olha"?

O algoritmo aprendeu padrões complexos, mas alguns fatores pesam mais:

1. **Engajamento Recente:** Se o cliente não loga há mais de 15 dias, o risco sobe exponencialmente.
2. **Satisfação:** Notas de avaliação de conteúdo abaixo de 3.0 são sinais de alerta.
3. **Financeiro:** Clientes com mensalidades muito altas sem uso proporcional tendem a cancelar.

### Níveis de Risco

O sistema classifica o risco em 3 faixas baseadas na probabilidade calculada:

| Classificação | Cor | Probabilidade | Ação Sugerida |
| :--- | :---: | :---: | :--- |
| **Crítico** | 🔴 | > 60% | Contato telefônico urgente / Oferta agressiva |
| **Alerta** | 🟠 | 42% - 60% | Envio de e-mail marketing / Push notification |
| **Seguro** | 🟢 | < 42% | Manter relacionamento padrão |

---

## ❓ 4. Perguntas Frequentes (FAQ)

**Q: O sistema exibe "Erro de Conexão com IA". O que fazer?**
**R:** Isso geralmente ocorre se o container Python (`ai-service`) estiver sobrecarregado ou reiniciando. Aguarde 30 segundos e tente novamente. O sistema possui *Auto-Healing* e se recupera sozinho.

**Q: Qual o limite de tamanho do arquivo CSV?**
**R:** Testamos com sucesso arquivos de até **100MB** (aprox. 500.000 linhas). Para arquivos maiores, sugerimos dividir em partes para evitar timeout no navegador.

**Q: Posso alterar a senha do admin?**
**R:** Nesta versão demonstrativa (Hackathon), a senha é fixa no Backend. Para produção, integramos com LDAP/OAuth.

---

**Equipe G8 - Hackathon Alura**
*Tecnologia e Dados a serviço da retenção.*
