# Prevenção de Churn em Assinantes de Streaming

![Imagem](https://cdn.telaviva.com.br/wp-content/uploads/2021/04/Cancel-e1688593083761.jpeg)

# -> LINKS

- [Repositorio](https://github.com/Araken13/ML-API-REST-HIBRIDA-HACKATHON-ONE-8)
- [Notebook Criação Dataset](./Dataset_Churn_Streaming_Hackathon.ipynb)
- [Dataset](https://raw.githubusercontent.com/rafaelreisramos/oracle-one-g8-hackathon/refs/heads/main/data/dados_streamingV4.csv)
- [Notebook EDA](./EDA_Streaming.ipynb)
- [Notebook Modelo](./Streaming_DS.ipynb)

# 1. Problema de Negócio

- Somos a Streaming, uma plataforma de streaming 100% brasileira focada em produções nacionais e esportes locais. Crescemos muito na pandemia, mas nos últimos meses, nossa taxa de cancelamento (Churn) disparou.

Não sabemos exatamente o porquê. Alguns dizem que é o preço, outros dizem que é o app travando em TVs antigas, ou a falta de conteúdo infantil.

Extraímos um dump do nosso banco de dados legado com 30.000 clientes. Atenção: Essa extração vem de sistemas diferentes (CRM, Billing e App de Analytics), então os dados não estão perfeitos, mas estamos enviando um Dicionario deles.

## Objetivo

- Limpar os dados, descobrir quem vai cancelar, gerar insights e  entregar uma API para que o time responsavel da empresa possa desenvolver estratégia antes que o cliente clique em 'Cancelar Assinatura'."

## Público-alvo

- Serviços de Streaming

----------------------------------------------------------------------------

# 2. Dicionário de Dados

## Fonte dos Dados

- Sintético.

## Descrição das Variáveis

- Uma tabela explicando o que cada coluna representa e sua unidade de medida.

**->`cliente_id`:**  Número de identificação único de cada cliente.

**->`churn`**  **TARGET (Variável Alvo):** Indica se o cliente cancelou (1) ou está ativo (0).

**->`idade`:**  Idade do cliente.

**->`genero`:** Gênero do cliente.

**->`regiao`:**  Região geográfica do Brasil do cliente.

**->`tipo_contrato`:**  Modalidade de cobrança do cliente: Mensal ou Anual.

**->`metodo_pagamento`:**  Forma como o cliente paga a assinatura.

**->`plano_assinatura`:**  Qual plano o cliente possui: Básico, Padrão ou Premium.

 **->`valor_mensal`:**  Valor da Mensalidade.

 **->`tempo_assinatura_meses`:**  Tempo em meses em que o cliente é assinante.

**->`dias_ultimo_acesso`:**  Número de dias desde o último acesso à plataforma.

**->`acessibilidade`:**  Se o cliente usou algum recurso de acessibilidade (0=Não, 1=Sim).

**->`contatos_suporte`:**  Quantidade total de contatos feitos com o suporte.

**->`visualizacoes_mes`:**  Total de conteúdo visualizado no último mês.

**->`tempo_medio_sessao_min`:**  Tempo médio de cada sessão de visualização em minutos.

**->`dispositivo_principal`:**  Dispositivo mais utilizado para visualizar o conteúdo.

**->`categoria_favorita`:**  Formato de conteúdo mais assistido.

**->`avaliacao_conteudo_media`:**  Média de avaliação de conteúdo durante todo o período do contrato. Se vazio cliente nao avaliou

**->`avaliacao_conteudo_ultimo_mes`:**  Avaliação média do conteúdo no último mês de assinatura. Se vazio cliente nao avaliou

**->`avaliacao_plataforma`:**  Avaliação média da plataforma pelo cliente. Se vazio cliente nao avaliou
----------------------------------------------------------------------

# 3. Metodologia e Ferramentas

## Tecnologias

- (Ex: Python, R, SQL, Power BI, Pandas, Scikit-learn).
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)](https://numpy.org/)
[![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-%23ffffff.svg?style=for-the-badge&logo=Matplotlib&logoColor=black)](https://matplotlib.org/)
 [![Seaborn](https://img.shields.io/badge/Seaborn-8B1A1A?style=for-the-badge&logo=python&logoColor=white)](https://seaborn.pydata.org/)
[![Jupyter Notebook](https://img.shields.io/badge/Jupyter-F37626.svg?style=for-the-badge&logo=Jupyter&logoColor=white)](https://jupyter.org/)

## Processo

- Breve descrição das etapas (Coleta, Limpeza, EDA, Modelagem).

------------------------------------------------------------------------------

# 4. Limpeza e Tratamento de Dados (Data Wrangling)

- Como foram tratados os valores ausentes (NaN)?
- Houve remoção de duplicatas ou outliers?
- Quais transformações de tipos de dados foram necessárias?
- Foram encontrados as seguintes colunas com valores missing:

-> `valiacao_conteudo_ultimo_mes`:  17.597

-> `valiacao_conteudo_media`: 11.777

-> `avaliacao_plataforma`: 6.041

-> `genero`: 3.000

## **`MÉTODO ADOTADO NO TRATAMENTO DOS VALORES MISSING`**

Considerando o problema de negócio, o dicionario de dados e a exploração dos dados. Optou-se por preencher todos os valore missing pelas seguintes justificativas e da seguinte forma:

### -> `Variável genero:`

Embora ela possa ser tratando no tipo *MNAR* por envolver perguntas pessoais, ela sera tratada como *MAR*(Missing at random; Missing aleatório). Pois se trata de uma variavel optativa, ou seja o cliente preenche se quer ou não e em principio não ha nenhum motivo para que ele preencha.

- Valor adotado: 'Nao_preenchido'

### -> Variáveis `avaliacao_conteudo_ultimo_mes`; `avaliacao_conteudo_media`; `avaliacao_plataforma`

Todas as variaveis foram tratadas como tipo *MNAR*(Not missing at random; Missing não aleatório), pois foi adotado as seguintes hipoteses:

1.**`Efeito do descontentamento extremo`**:
"Não vou perder tempo respondendo"
Resultado: Missing super-representa notas baixas

2.**`Efeito da satisfação extrema`**:
"Já estou tão satisfeito que não preciso reclamar/elogiar"
Resultado: Missing super-representa notas altas

3.**`Efeito da indiferença`**:
"Tanto faz, não respondo"
Resultado: Missing super-representa notas médias

- Valor adotado: `Nao_preenchido`

-----------------------------------------------------------------

# 5. Análise Exploratória (EDA)

## -> **ANÁLISE A VARIÁVEL TARGET (CHURN)**

### 1. Na `análise de churn` do conjunto de dados, `24,9% (7.471 clientes) cancelaram o serviço`, enquanto `75,1% (22.528 clientes) permanecem ativos`

![Imagem](https://github.com/JeanKahlilR/Hackathon-One/blob/main/Grafico%20propor%C3%A7%C3%A3o%20de%20churn.png?raw=true)

### 2 .Na análise por `cohort` (retensão pelo tempo de assinatura), identificou-se uma taxa de `retenção mínima de 64,7%` e `máxima de 93,2%`. Foi observado que a retenção é mais baixa entre o primeiro e o quarto mês, além de um ponto `crítico de queda na retenção no 38º mês`

![Imagem](https://github.com/JeanKahlilR/Hackathon-One/blob/main/Grafico%20corhot.png?raw=true)

## -> **ANALISE DEMOGRAFICA DE CADASTRO**

### 1.O Gráfico  que detalha a `distribuição do churn por gênero`, revela um achado estratégico importante: a taxa de evasão é praticamente homogênea entre todas as categorias, variando apenas entre 23,1% e 25,7%

### Isso indica que, dentro do escopo desta análise, o gênero do cliente não é um fator discriminante ou preditor forte para o cancelamento. Portanto, as campanhas e estratégias de retenção não precisam ser segmentadas por esse atributo, permitindo um foco mais direcionado em outros drivers de churn (como tempo de assinatura, motivo de cancelamento ou tipo de plano)

### Observação Técnica: *A base contém um volume relevante de registros com gênero 'Não_preenchido' ou 'Não Informar' (n=5.159), o que representa uma oportunidade para melhorar a completude dos dados e refinar futuras análises.*

![Imagem](https://github.com/JeanKahlilR/Hackathon-One/blob/main/Grafico%20Churn%20por%20Genero.png?raw=true)

### 2. Comparação de Médias: A análise inicial não revela um padrão claro de churn pela idade central. A média de idade dos clientes que cancelaram (37,9 anos) é virtualmente idêntica à dos clientes ativos (37,8 anos), indicando que, em termos gerais, a idade não é um discriminante

### Análise por Faixas Etárias: Um olhar mais detalhado por segmentos mostra uma leve variação. A taxa de churn atinge um pico de 26,1% na faixa de 56 a 65 anos, sendo mais baixa (22,1%) entre clientes com mais de 66 anos. Essa diferença de 4 pontos percentuais, embora existente, é considerada baixa dentro do contexto do negócio

### Com base nos dados disponíveis, a idade não se mostra uma variável preditora forte ou isolada para a evasão. A diferença mínima nas médias e a baixa amplitude nas taxas por faixa etária corroboram essa visão

![Imagem](https://github.com/JeanKahlilR/Hackathon-One/blob/main/Grafico%20Churn%20por%20Idade.png?raw=true)

### 3. Para aprofundar a análise da relação entre idade e churn, segmentou-se a base nas gerações: Z, Millennials, X, Baby Boomers e Silenciosa. A Geração Silenciosa (acima de 80 anos) apresenta taxa de churn atípica (14,3%), significativamente abaixo da média geral (24,9%). No entanto, este grupo representa uma amostra mínima (21 clientes), limitando a inferência. As demais gerações, que constituem a quase totalidade da base, apresentam taxas de churn muito próximas, variando entre 24,6% (Z) e 26,7% (Baby Boomers). Esse padrão reforça que a idade, por si só, não é um fator explicativo relevante para o cancelamento

![Imagem](https://github.com/JeanKahlilR/Hackathon-One/blob/main/Grafico%20Churn%20por%20Gera%C3%A7%C3%B5es.png?raw=true)

### 4.Análise Geográfica Revela Churn como um Desafio Nacional Uniforme. A análise das taxas de churn por macro-região do Brasil, conforme detalhado no Mapa de Calor, revela uma distribuição notavelmente homogênea. Todas as cinco regiões apresentam taxas contidas em uma estreita faixa de apenas 2,4 pontos percentuais (mínima de 22,7% no Norte e máxima de 25,1% no Sul)

### Esta mínima variação regional demonstra que o churn é um fenômeno disseminado e uniforme em todo o território nacional. A causa do cancelamento não está associada a variáveis locais específicas (como oferta regional de concorrentes ou aspectos culturais marcantes que impactem a retenção de forma desigual)

![Imagem](https://github.com/JeanKahlilR/Hackathon-One/blob/main/Grafico%20Mapa%20de%20Calor%20Regi%C3%B5es.png?raw=true)

### 5. Nas análises de churn por tipo de contrato e plano de assinatura, identificaram-se diferenças marcantes

### -Tipo de Contrato: Clientes com contrato anual têm uma taxa de churn de 13,2%, menos da metade da taxa observada para clientes no plano mensal (29,5%)

### -Plano de Assinatura: O plano Premium apresenta a menor taxa de churn (15,1%), enquanto o plano Básico tem a mais alta (29,1%), praticamente o dobro

### Os resultados sugerem uma correlação forte entre o cancelamento e essas duas variáveis, sendo esta a primeira relação clara e significativa identificada no estudo

![Imagem](https://github.com/JeanKahlilR/Hackathon-One/blob/main/Grafico%20Taxa%20de%20Churn%20por%20Tipo%20de%20Contrato.png?raw=true)
![Imagem](https://github.com/JeanKahlilR/Hackathon-One/blob/main/Grafico%20An%C3%A1lise%20de%20Planos%20de%20Assinatura%20vs%20Churn.png?raw=true)
![Imagem](https://github.com/JeanKahlilR/Hackathon-One/blob/main/Grafico%20An%C3%A1lise%20Valor%20Mensal%20vs%20Tempo%20de%20Contrato.png?raw=true)

## -> **ANALISE DE COMPORTAMENTO DE USO**

### 1.Na análise comportamental, o tempo desde o último acesso à plataforma demonstrou ser um preditor extremamente forte de cancelamento. A taxa de churn escala drasticamente conforme a inatividade aumenta, atingindo 81,7% para clientes que não acessam há mais de 60 dias. Isso confirma uma correlação direta e muito significativa

![Imagem](https://github.com/JeanKahlilR/Hackathon-One/blob/main/Grafico%20An%C3%A1lise%20de%20Risco%20Baseada%20em%20%C3%9Altimo%20Acesso.png?raw=true)
![Imagem](https://github.com/JeanKahlilR/Hackathon-One/blob/main/Grafico%20metricas%20por%20cataegoria%20de%20acesso.png?raw=true)

### 2. A análise do comportamento na plataforma indica que o engajamento medido é um dos princiapis sintomas da saúde do cliente. As diferenças entre clientes ativos e que cancelaram são altos e fornecem limites visiveis para ação

### Evidências Quantitativas

### - Visualizações/Mês: Clientes ativos consomem, em média, 36 conteúdos/mês. Clientes que cancelaram consumiam apenas 3, uma queda de 92%

### - Tempo de Sessão: A média cai de 74 minutos (ativos) para 20 minutos (churn)

### - Taxa de Churn por Categoria: O efeito é categórico. Clientes classificados com engajamento "Baixo" têm uma taxa de churn de 86.9%, tornando o cancelamento proximo de  uma certeza estatística

### Não é uma correlação sutil; é um limiar bem estabelecido. Existe um ponto de alerta no engajamento, abaixo do qual a perda do cliente é quase que certa

![Imagem](https://github.com/JeanKahlilR/Hackathon-One/blob/main/AN%C3%81LISE%20DE%20ENGAJAMENTO%20VISUALIZA%C3%87%C3%95ES%20vs%20TEMPO%20DE%20SESS%C3%83O.png?raw=true)

### 3. Na análise de churn por categoria de conteúdo favorita, não foi identificada nenhuma métrica que indique uma influência significativa do tipo de conteúdo na decisão de cancelamento. Todas as categorias apresentam taxas de churn muito próximas, variando entre 24,1% e 25,4%, em torno da média geral de 24,9%

![Imagem](https://github.com/JeanKahlilR/Hackathon-One/blob/main/Grafico%20An%C3%A1lise%20de%20Churn%20por%20Categoria%20Favorita%20de%20Conte%C3%BAdo.png?raw=true)

### 4. A análise de contatos com o suporte, quantifica de forma clara o impacto da experiência com o suporte na retenção de clientes. A taxa de churn escala drasticamente com o número de contatos, revelando um processo  de insatisfação acumulada

### Evidências Quantitativas

### - 0 Contatos: Churn de 17,8% (abaixo da média de 24,9%)

### - 1 Contato: Churn salta para 28,6% – um aumento de 61% em relação ao grupo anterior

### - 3 Contatos: Churn atinge o pico de 46,4%, indicando que problemas não resolvidos levam quase metade dos clientes a cancelar

### O primeiro contato com o suporte é um ponto de virada (tipping point). Um cliente que precisa abrir um chamado já vê sua probabilidade de cancelar aumentar em mais de 10 pontos percentuais. Isso transforma o suporte de um centro de custo em uma frente estratégica de retenção

![Imagem](https://github.com/JeanKahlilR/Hackathon-One/blob/main/Grafico%20An%C3%A1lise%20Contatos%20com%20Suporte%20vs%20Churn.png?raw=true)
![Imagem](https://github.com/JeanKahlilR/Hackathon-One/blob/main/Grafico%20An%C3%A1lise%20de%20Risco%20Detalhada.png?raw=true)

## -> **ANÁLISE DE AVALIAÇÕES E SATISFAÇÃO**

### 1. A análise das avaliações de conteúdo revelou uma correlação muito forte com o cancelamento, atuando como um termômetro  da satisfação do cliente

### Observou-se que

### - Clientes que nunca avaliaram qualquer conteúdo apresentam uma taxa de churn elevadíssima de 31,3%, além de métricas de engajamento (tempo de sessão, visualizações) inferiores às médias

### - A tendência da avaliação é ainda mais reveladora: enquanto uma melhora na nota está associada a um churn mínimo (2,8%), uma queda significativa (>2 pontos) leva a uma taxa de cancelamento de 42,7%

### Esses padrões confirmam que o comportamento de avaliação é um indicador preditivo valioso e merece ser aprofundado em análises futuras

![Imagem](https://github.com/JeanKahlilR/Hackathon-One/blob/main/Grafico%20An%C3%A1lise%20Queda%20nas%20Avalia%C3%A7%C3%B5es%20como%20Sinal%20de%20Alerta.png?raw=true)
![Imagem](https://github.com/JeanKahlilR/Hackathon-One/blob/main/Grafico%20An%C3%A1lise%20Clientes%20que%20Nunca%20Avaliaram%20o%20Conte%C3%BAdo.png?raw=true)
![Imagem](https://github.com/JeanKahlilR/Hackathon-One/blob/main/Grafico%20Vis%C3%A3o%20Geral%20Categorias%20de%20Avalia%C3%A7%C3%A3o%20vs%20Churn.png?raw=true)

### 2. Contrariando uma possível intuição, a avaliação geral que o cliente atribui à plataforma não apresenta correlação com a decisão de cancelar. Como demonstrado no gráfico, a taxa de churn permanece estável em torno da média (24,9%), independentemente de a classificação ser "Boa" (25,2%) ou "Muito Boa" (24,0%)

![Imagem](https://github.com/JeanKahlilR/Hackathon-One/blob/main/Grafico%20Rela%C3%A7%C3%A3o%20Direta%20Avalia%C3%A7%C3%A3o%20da%20Plataforma%20vs%20Churn.png?raw=true)

## -> **ANÁLISE DE PAGAMENTOS E TRANSAÇÕES**

### 1. A análise da forma de pagamento revela que a escolha do método de pagamento é um fator importante para a retenção, com uma variação extrema de 28,6 pontos percentuais entre a melhor (Crédito Recorrente) e a pior (Boleto) opção

### Achados Quantitativos

### -Boleto (47,2% churn): Mais que o dobro da taxa de clientes com Crédito Recorrente. Representa uma experiência de pagamento falha

### -Crédito Recorrente (18,6% churn): O método mais eficaz para retenção, com churn 14,7 p.p. abaixo da média e 28,6 p.p. abaixo do Boleto

### - Outros Métodos (Cartão, Débito): Churn elevado (~31%), indicando que a simples presença de uma cobrança manual ou a necessidade de reter os dados do cartão já é um ponto de atrito

![Imagem](https://github.com/JeanKahlilR/Hackathon-One/blob/main/Grafico%20An%C3%A1lise%20de%20Churn%20por%20M%C3%A9todo%20de%20Pagamento.png?raw=true)
![Imagem](https://github.com/JeanKahlilR/Hackathon-One/blob/main/Grafico%20Cr%C3%A9dito%20Recorrente%20vs%20Outros%20M%C3%A9todos.png?raw=true)

## -> **PRINCIPAIS INSIGHTS**

### - `Compromisso vs. Flexibilidade`: Contratos anuais criam uma barreira a saída e oferecem valores atrativos, atraindo assim clientes mais comprometidos

### - `Percepção de Valor`: Planos superiores (Premium) podem oferecer mais benefícios ou ter clientes com maior satisfação e envolvimento

### - `Inatividade na Plataforma`: Monitorar o último acesso não é apenas uma métrica de uso, mas um termômetro da saúde do cliente. Implementar ações baseadas nesse indicador terá o retorno mais direto e mensurável na redução do churn

### - `Engajamento, um sinal vital`: Ha um limiar claro no engajamento, quanto maior o tempo de inatividade, maior maior a possibilidade de cancelamento, chegando a niveis quase estatisticamente certos de que ocorrera o churn

### - `Experiência com o Suporte, Um Driver Crítico e Mensurável de Insatisfação e Churn`: O primeiro contato com o suporte é um ponto de virada (tipping point). Um cliente que precisa abrir um chamado já vê sua probabilidade de cancelar aumentar em mais de 10 pontos percentuais. Isso transforma o suporte de um centro de custo em uma frente estratégica de retenção

### - `Avaliações de Conteúdo. O Sistema de Alerta de Satisfação Mais Direto para Prever Churn`: As avaliações vão além de um simples feedback de conteúdo; são um reflexo direto da saúde do relacionamento com o cliente. Implementar um processo de escuta ativa e resposta a esses sinais é uma das formas mais eficientes de reduzir churn de forma preventiva.  A análise de avaliações oferece um sistema de alerta em três camadas: 1) Cliente nunca deu feedback (risco), 2) Cliente piorou sua avaliação (alerta vermelho), 3) Cliente dá nota consistentemente baixa (insatisfação crônica)

### - `Método de Pagamento. Um dosDrivers Operacionais de Churn`:  Otimizar o método de pagamento é uma das alavancas  para reduzir o churn operacional. A migração  para o Crédito Recorrente deve ser uma iniciativa prioritária de negócio, com potencial de reduzir a taxa geral de churn de forma significativa

## -> **CONCLUSÕES E RECOMENDAÇÕES**

Com base na análise e nas evidências, recomenda-se um plano de ação focado em três pilares:

### - `PILAR 1`: OTIMIZAR O MODELO COMERCIAL

### Objetivo: Reduzir a fricção operacional e aumentar o compromisso de longo prazo

### 1. Migrar para Contrato Anual: Criar um programa de incentivos (ex.: 2 meses gratuitos no primeiro ano) para converter clientes mensais em anuais

### 2. Revisar a Proposta de Valor do Plano Básico: Investigar causas do alto churn (ex.: limite de conteúdo, qualidade). Considerar unificar os planos Básico e Padrão ou criar um caminho de upsell mais eficiente

### - `PILAR 2`: IMPLEMENTAR UM SISTEMA PREDITIVO DE ALERTA

### Objetivo: Identificar e agir sobre clientes em risco antes do cancelamento

### 1. Criar um "Score de Risco" Baseado em Comportamento: Desenvolver um modelo simples que pontue clientes clusterisando com base em

- Dias desde o último acesso
- Queda no engajamento
- Queda nas avaliações de conteúdo
- Contato recente com o suporte.

### 2. Automatizar Fluxos de Reengajamento

- Alerta Amarelo (Risco Médio): Disparar sequências automatizadas de e-mail com conteúdo personalizado e ofertas de reengajamento.
- Alerta Vermelho (Alto Risco): Atribuir ao time de Customer Success para contato proativo e oferta de retenção personalizada.

### - `PILAR 3`:  TRANSFORMAR O SUPORTE EM CENTRO DE RETENÇÃO

### Objetivo: Resolver problemas na primeira interação e reter clientes insatisfeitos

### 1. Focar na Resolução no Primeiro Contato (FCR): Tornar esta a métrica-chave do time. Investir em treinamento e ferramentas para os agentes

### 2.Criar um Processo de Escalonamento para Clientes Insatisfeitos: Clientes que abrirem um segundo chamado sobre o mesmo assunto devem ser automaticamente direcionados a um especialista sênior ou ao time de retenção

### 3. Integrar o Feedback ao Produto: Canalizar as principais causas de contato (ex.: problema técnico recorrente, dificuldade de navegação) para as equipes de produto e engenharia como itens prioritários de correção

## -> **PROXIMOS PASSOS**

### **ANÁLISE MULTIVARIADA E CORRELAÇÕES, ENGENHARIA DE FEATURES E HIPÓTESES**

### `Objetivo`: Identificar relações complexas e preparar os dados para um modelo preditivo

### 1.Matriz de Correlação

- Apenas para variáveis numéricas
- Destacar correlações com churn

### 2.Análise de Segmentos

- Clusterização simples (K-means) para identificar perfis
- Personas de risco de churn

### 3. Interações entre Variáveis

- Ex:  Plano+ visualizações
- Ex: Contatos suporte + dispositivo principal
- Ex: Categoria Favorita + Avaliação do conteudo

### 4. Criação de Features

- Ex: Razão uso/valor (ROI percebido)
- Ex: Clusterização dias do ultimo acesso (Baixo, Médio, Alto, Elevado)
- Ex: Clusterização do tempo médio de seção (Baixo, Médio, Alto, Elevado)

### 5. Teste de Hipóteses do Negócio

- H1: "O preço causa churn"
- H2: "Falta de avaliação causa churn"
- H3: "Contato com suporte causa churn"

-------------------------------------------------------------------------------

### Resultados

- Resumo do que foi descoberto em relação ao objetivo inicial.

### Ações Sugeridas

- Com base nos dados, o que a empresa ou o usuário deve fazer?

## 7. Como Executar o Projeto

### Pré-requisitos

- Bibliotecas necessárias ou versões de software.

### Instruções

- Passo a passo para rodar o código localmente.

--------------------------------------------------------------------

# 6.  Relatório Data Science

## -> **INTRODUÇÃO E METODOLOGIA**

Este relatório apresenta o desenvolvimento de um **modelo preditivo** de alta precisão para identificar o
**Churn de clientes no setor de streaming**. A metodologia seguiu etapas rigorosas de pré-processamento,
modelagem e validação final.

## -> **PREPARAÇÃO E ESTRATIFICAÇÃO DOS DADOS**

- `Processamento Inicial:` O dataset original de 30.000 registros passou por limpeza e criação de flags MNAR para variáveis de avaliação, preservando o valor informacional dos dados ausentes.
- `Divisão do Dataset:` Os dados foram segmentados em Treino (21.600), Teste (5.400) e Validação (3.000), garantindo uma prova real (holdout) isenta de vazamentos.

## -> **OTIMIZAÇÃO E CALIBRAÇÃO DO MODELO**

- `Seleção de Atributos:` O método RFE selecionou as 25 variáveis mais impactantes.
- `Hiperparâmetros:` Via GridSearchCV, o modelo Random Forest foi otimizado (F1-Score: 0.9482), priorizando o peso da classe Churn para mitigar falsos negativos.
- `Confiabilidade:` A calibração isotônica ajustou as probabilidades, definindo o threshold ótimo em 0.5698.

## -> **PERFORMANCE E ROBUSTEZ**

O modelo atingiu níveis de excelência com alta consistência entre os ambientes:

- `F1-Score (Validação):` 0.9531.
- `ROC-AUC:` 0.9957.
- `Estabilidade:` Deltas mínimos (< 0.003) entre teste e validação confirmam a robustez do aprendizado.

![Imagem](https://github.com/JeanKahlilR/Hackathon-One/blob/main/validacao.png?raw=true)

## -> **INTELIGÊNCIA DE NEGÓCIO**

A análise identificou que apenas 12 variáveis explicam 80% do modelo. `Os 5 principais drivers representam 80.9%` do poder preditivo:

- `Engajamento Score:` 29.43%
- `Tempo Médio de Sessão:` 26.62%
- `Avaliação de Conteúdo (Média):` 8.62%
- `Avaliação de Conteúdo Ultimo Mês:` 8.2%
- `Vizualizações no Mês:` 8.0%
![Imagem](https://github.com/JeanKahlilR/Hackathon-One/blob/main/feature_importance.png?raw=true)
