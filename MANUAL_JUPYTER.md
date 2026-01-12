# 📘 Manual de Operação via Jupyter Notebook

## ChurnInsight AI - Hackathon Alura 2026

Este documento orienta sobre como controlar **todo o ciclo de vida do projeto** (Infraestrutura, API e Testes) utilizando exclusivamente o **Jupyter Notebook** como painel de controle.

Isso ideal para apresentações, demos ao vivo e validações rápidas.

---

### 📂 Arquivos Importantes

1. **`Controlador_Do_Projeto.ipynb`**: O "cérebro" da operação. Sobe infra e API.
2. **`Demo_Interativa_API.ipynb`**: O "cliente". Consome a API e gera gráficos.
3. **`teste_batch.csv`**: Arquivo de dados para teste rápido.

---

### 🚀 Fluxo 1: Rodando TUDO pelo Notebook (Recomendado para Demos)

Se a máquina estiver "limpa" (sem API rodando no terminal), siga este passo a passo:

1. **Abra o arquivo** `Controlador_Do_Projeto.ipynb` no VS Code.
2. **Execute a Célula 1 ("Reiniciar Containers")**:
   - Isso vai garantir que o MongoDB e o AI Service (Python) estejam zerados e rodando via Docker.
3. **Execute a Célula 2 ("Iniciar API Java")**:
   - VAI INICIAR O SERVIDOR JAVA EM BACKGROUND.
   - **Atenção**: Uma bolinha de carregamento pode ficar girando ou terminar rápido dizendo "Processo iniciado". Isso é normal.
4. **Execute a Célula 3 ("Healthcheck")**:
   - Esta célula ficará rodando (pingando) até a API responder "Estou Oline".
   - Só pule para a próxima etapa quando ver: `✅ API ONLINE!`.
5. **Execute a Célula 4 ("Pipeline de Testes")**:
   - Faz Login automático.
   - Envia o CSV.
   - Mostra a tabela de resultados com as previsões de Churn.
6. **Ao finalizar, execute a Célula 5**:
   - Isso mata o processo Java e desliga o Docker para liberar memória.

---

### ⚡ Fluxo 2: Modo Híbrido (Terminal + Notebook)

Se você prefere ver o log colorido do Spring Boot no terminal:

1. **No Terminal**:
   - Inicie o Docker: `docker-compose up -d`
   - Inicie a API: `.\run_api.bat`
   - Aguarde aparecer "Started ChurnGraphqlApiApplication".

2. **No Notebook (`Demo_Interativa_API.ipynb`)**:
   - Pule as etapas de infraestrutura.
   - Use apenas as células de **Autenticação**, **GraphQL** e **Gráficos**.

---

### ⚠️ Solução de Problemas Comuns

| Problema | Causa Provável | Solução |
|:--- |:--- |:--- |
| **Erro "BindingException: Address already in use"** | A API já está rodando em outro terminal ou notebook. | Execute a **Célula 5** para matar processos Java ou feche os terminais abertos. |
| **Timeout aguardando API** | O Java está demorando para compilar ou o Docker não subiu. | Verifique se o Docker Desktop está verde. Tente rodar `docker ps` no terminal. |
| **Erro de "ModuleNotFoundError"** | Faltam bibliotecas Python. | Instale rodando uma célula com: `!pip install requests pandas matplotlib` |

---

### 📊 Exemplo de Apresentação (Script de Fala)

1. *"Vou iniciar toda a infraestrutura do nosso banco e modelo de IA com um clique..."* (Roda Célula 1)
2. *"Agora, subimos nossa API Java robusta para orquestrar tudo..."* (Roda Célula 2)
3. *"O sistema faz um healthcheck automático para garantir disponibilidade..."* (Roda Célula 3)
4. *"Finalmente, vamos processar um lote de clientes e ver quem vai dar Churn..."* (Roda Célula 4)
