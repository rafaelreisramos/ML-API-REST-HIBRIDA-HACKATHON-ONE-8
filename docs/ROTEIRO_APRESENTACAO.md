# 🎙️ Roteiro de Apresentação: ChurnInsight (5 Minutos)

Este roteiro foi desenhado para destacar a robustez técnica, a arquitetura moderna e a facilidade de uso da solução **ChurnInsight**.

---

## 🏗️ Preparação (Antes de começar)

Certifique-se de ter os containers ativos para não perder tempo com build na hora.

1. `docker-compose -f docker-compose.local.yml up -d`

---

## ⏱️ Minuto 1: O "Setup Mágico" (Developer Experience)

**Objetivo:** Mostrar que o projeto é organizado e fácil de iniciar.

1. **Ação:** Abra o terminal na pasta raiz e diga: *"Vamos começar do zero."*
2. **Comando:** (Simule o clone ou já esteja na pasta)

   ```bash
   git clone https://github.com/RRdOD/hackathon_g8_one.git
   ```

3. **O "Pulo do Gato":** Execute a ferramenta de apresentação local que valida todo o ambiente.

   ```powershell
   powershell -ExecutionPolicy Bypass -File developer_tools/scripts/presentation_cover_local.ps1
   ```

4. **Narrativa:**
   > *"Em vez de rodar testes manuais, criamos uma CLI interativa. Vou selecionar a **Opção 1 (Validação Técnica)**. O sistema autodetecta que estamos rodando Localmente, isola a nuvem OCI e verifica: Conectividade, Banco de Dados, API GraphQL e o Modelo de IA. Tudo verde, estamos prontos."*

---

## ⏱️ Minuto 2: A Solução (Frontend & Dashboard)

**Objetivo:** Impacto visual e valor de negócio.

1. **Ação:** Abra o navegador em `http://localhost:3000`.
2. **Login:** User: `admin` | Senha: `123456`.
3. **Tela:** Dashboard Principal.
4. **Narrativa:**
   > *"Este é o **ChurnInsight**. Um dashboard em tempo real construído com React e Tailwind. O diferencial aqui não é só a beleza, é a **Arquitetura Híbrida**. O Frontend consome uma API **GraphQL** no Backend Java, que por sua vez orquestra um microsserviço Python onde vive a nossa Inteligência Artificial."*

**Destaque (Diferencial):** Aponte para as métricas de "Risco Médio". Explique que isso não é conta de padaria, é um modelo **Random Forest** analisando comportamento do usuário.

---

## ⏱️ Minuto 3: Simulador & Poder da IA

**Objetivo:** Demonstrar a interatividade e a inteligência do modelo.

1. **Ação:** Clique na aba **"Simulador"**.
2. **Interação:** Preencha um perfil de risco (Ex: Pouco uso, nota baixa, acesso antigo).
3. **Clique:** "Calcular Risco".
4. **Simulação:** Altere um campo (Ex: Aumente a "Avaliação" para 5) e recalcule.
5. **Narrativa:**
   > *"Isso empodera o time de Suporte. Eles podem simular cenários: 'Se dermos um desconto ou melhorarmos o atendimento, o cliente fica?'. A IA responde na hora: 'Sim, o risco cai de 80% para 20%'. É inteligência acionável."*

---

## ⏱️ Minuto 4: Alta Performance (Batch Upload)

**Objetivo:** Provar que o sistema aguenta carga real.

1. **Ação:** Vá para a aba **"Batch Upload"**.
2. **Demo:** Arraste o arquivo `teste_batch_100.csv` (localizado em `docs/csv`).
3. **Resultado:** Mostre a barra de progresso e o download automático.
4. **Narrativa:**
   > *"E para o time de Dados? Não analisamos um por um. Processamos lotes massivos. Nossa arquitetura suporta milhares de registros via processamento assíncrono e paralelo. O sistema ingere o CSV, paraleliza as predições na IA e devolve o relatório enriquecido."*

---

## ⏱️ Minuto 5: Arquitetura & Encerramento

**Objetivo:** Fechar com autoridade técnica.

1. **Mostre o Diagrama (Opcional):** Se der tempo, abra o arquivo `docs/ARCHITECTURE.md` ou apenas fale.
2. **Pontos Chave para Falar:**
   * **Híbrido:** *"O mesmo código roda no meu laptop e na Oracle Cloud Infrastructure (OCI) sem mudar uma linha."*
   * **Flexível:** *"Usamos Docker para garantir que o ambiente Python da IA e o Java do Backend sejam imutáveis."*
   * **Seguro:** *"Autenticação JWT completa."*
3. **Encerramento:**
   > *"O ChurnInsight une a robustez do Java, a flexibilidade do Python e a modernidade do React para resolver um problema real de negócio: reter clientes. O repositório está documentado, testado e pronto para deploy. Obrigado."*

---

### 📋 Checklist de Arquivos para a Demo

* [ ] Repositório clonado.
* [ ] Docker rodando.
* [ ] Arquivo `teste_batch_100.csv` acessível (arraste para o Desktop antes).
* [ ] Script `presentation_cover_local.ps1` testado.
