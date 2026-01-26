**Churn Insight by ExodIA**  
*Um estudo de caso de Monitoramento de Risco de Cancelamento para a Brasil Streaming*

Nossa empresa, ExodIA, foi procurada pela Brasil Streaming para enfrentar um desafio crítico: a evasão de clientes.

Ela conhecia nosso trabalho com análise de evasão em empresas de telecomunicações e queria aplicar nossa expertise para reduzir a evasão na plataforma de streaming.

Eles nos explicaram que gostariam de desenvolver um modelo preditivo que fosse capaz de identificar usuários com alto risco de cancelar suas assinaturas e permitisse ações proativas de retenção.

A ideia deles era disponibilizar esse modelo aos times de Customer Success, tanto na área de atendimento ao cliente quanto na área de marketing, para que pudessem implementar campanhas de retenção personalizadas.

Eles nos informaram que tinham uma base de dados histórica com informações sobre os usuários da plataforma, incluindo dados demográficos, padrões de uso, interações com o conteúdo e histórico de cancelamentos.

Deixaram evidente que a base não estava limpa, apresentando dados ausentes e inconsistências devido a algumas trocas problemáticas de sistema ao longo do tempo.

A base não era a totalidade dos usuários, mas sim uma amostra representativa.

Tão logo fechamos o projeto, após as assinaturas do NDA e contrato, iniciamos a fase de descoberta e exploração dos dados para entender sua estrutura, qualidade e disponibilidade.

Na nossa análise inicial, verificamos que a taxa de evasão na amostra era de 24,9%, ou seja, quase 1 em cada 4 usuários havia cancelado suas assinaturas.

Existia a oportunidade de oferecer uma ferramenta que permitisse visualizar a predisposição do comportamento do usuário e reduzir essa taxa com ações proativas antes do "adeus". De forma alguma reduziríamos a evasão a zero, mas poderíamos diminuí-la de forma significativa.

Reunimos então a equipe da ExodIA, composta pela equipe de ciência de dados e pela equipe de desenvolvimento web, para definir a arquitetura da solução.

Decidimos que iríamos disponibilizar uma interface web amigável para os times de Customer Success, onde eles podem consultar o risco de evasão dos usuários individualmente ou em lotes; um modelo robusto de predição com uma proposta de revalidação à medida que os dados evoluem ou a predição da evasão falha; além de uma API RESTful para integração com os sistemas existentes da Brasil Streaming.

Em resumo, a estrutura ficou assim: uma API RESTful que receberia os dados dos usuários, retornaria a predição de risco de evasão e armazenaria os dados de consulta. Como uma funcionalidade adicional de resposta a falhas, faria um retreinamento do modelo no caso da perda de comunicação com o micro serviço de Machine Learning, Um micro serviço de Machine Learning. Esse micro serviço hospedaria o modelo preditivo com as regras de retreinamento em caso de deterioração da performance. Finalmente, uma interface web amigável para os times de Customer Success. Tudo isso armazenado em uma estrutura de nuvem robusta, segura e escalável da Oracle Cloud.

A equipe de dados iniciou então a fase de exploração e preparação, onde foram tratados os dados ausentes, removidas as inconsistências e criadas novas features preditivas. Em paralelo, a equipe de desenvolvimento iniciou a construção da API RESTful e da interface web a partir de um mockup do modelo de predição.

Na exploração dos dados, a equipe de Data Science identificou que muitos dados faltantes não eram simplesmente ausentes, mas sim dados ausentes com significado (MNAR \- Missing Not At Random). Os efeitos desses dados sugeriam diferentes comportamentos dos usuários, dependendo do contexto. Às vezes, poderia indicar um descontentamento extremo; em outras, uma satisfação extrema ou até uma indiferença total. Cada um desses contextos impactava de forma distinta a predição de evasão. Por exemplo, a ausência de avaliações por parte dos usuários era um forte indicador de desinteresse e possível evasão futura.

Decidimos, então, tratar esses dados de forma especial, criando uma feature binária que indicava a ausência de avaliações, o que se mostrou altamente preditivo.

Duas variáveis se destacaram na análise dos dados: a forma de pagamento e a quantidade de contatos com o suporte ao cliente. Usuários que pagavam com boleto e os com menor avaliação na plataforma, combinados com a entrada em em contato com o suporte mais de três vezes nos últimos meses, apresentavam risco significativamente maior de evasão.

As variáveis demográficas, como idade, gênero e região, pareciam ter um impacto menor na predição, mas foram mantidas para a avaliação nos modelos para garantir uma visão completa do perfil do usuário.

Temos uma série de gráficos e análises detalhadas no projeto, mas aqui vamos focar nos pontos principais.

Enquanto isso, a equipe de desenvolvimento avançava na construção da API RESTful, definindo os endpoints para consultas individuais e em lote, além de implementar a autenticação e autorização com JWT e suporte SSL para garantir a segurança dos dados.

Durante esta fase do desenvolvimento, as equipes foram muito resilientes e colaborativas, trabalhando em sinergia. Tivemos problemas com colegas que se desligaram da empresa no meio do projeto, mas conseguimos superar esses desafios por meio de planejamento e comunicação eficaz. Sofremos também com colegas que adoeceram e tiveram problemas pessoais, o que impediu uma participação mais ativa, mas a equipe se uniu para garantir que o projeto continuasse avançando.

É difícil demonstrar todos os detalhes técnicos do processo de modelagem, mas, em resumo, após a preparação dos dados, a equipe de Data Science testou vários modelos preditivos, incluindo Regressão Logística, Gradient Boosting e Random Forest.

Após uma série de testes e validações cruzadas, o modelo de Random Forest destacou-se como o mais eficaz, apresentando um equilíbrio ideal entre precisão e recall.

Com a seleção do modelo, foram identificadas as features mais importantes para a predição, sendo o Engagement Score (29,4%), o Tempo de Sessão (26,6%) e a Ausência de Avaliações média, Ausência de Avaliações no Último Mês e Visualizações no mês, com cerca de 8% cada, que explicam quase 80% do impacto total do modelo.

Essas variáveis, que indicam que o comportamento do usuário dentro da plataforma, levaram o modelo de predição a um patamar ótimo, sem qualquer sinal de overfitting.

O modelo final apresentou uma performance de elite, com um F1-Score de 0,95, Recall de 96,9% e ROC-AUC de 0,995, indicando separação quase perfeita entre os usuários que iriam cancelar e os que permaneceriam.

Essas métricas indicam que o modelo é altamente eficaz em identificar usuários com risco alto de evasão, permitindo ações proativas de retenção.

Já a equipe de desenvolvimento finalizou a API RESTful, garantindo que ela fosse robusta, segura e escalável. A autenticação com JWT e o suporte a SSL foram implementados com sucesso, permitindo que apenas usuários autorizados acessassem os dados sensíveis. As pools de tarefas permitem o upload de arquivos em lotes de tamanho significativo, sem bloquear o servidor e a responsividade da API às demais requisições.

A implementação dual do armazenamento em memória permite a atualização em tempo real do dashboard, e a persistência dos dados em um banco relacional garante a integridade e disponibilidade dos dados para análises futuras.

A infraestrutura implementada na nuvem prevê resiliência e autocura com o uso de containers Docker, orquestrados com medições de saúde.

Com o modelo finalizado e a API RESTful pronta, a equipe de Data Science e desenvolvimento trabalhou junta para integrar o modelo preditivo na API. A integração foi realizada com sucesso, permitindo que o sistema retornasse as predições de risco de evasão em tempo real.

Com base na solução implementada, sugerimos uma estratégia de retenção em três fases:

\- Usuários com score de risco inferior a 30% receberiam um alerta imediato encaminhado ao time de Customer Success, que poderia contactá-los proativamente para compreender suas preocupações e oferecer soluções  personalizadas.

\- Para usuários que apresentarem sinais de inatividade silenciosa, campanhas automáticas  de reengajamento serão disparadas, oferecendo incentivos personalizados para  estimular o uso da plataforma.

\- Finalmente, um aprimoramento do monitoramento contínuo do modelo seria implementado  para detectar qualquer deterioração na performance, permitindo retreinamentos regulares  para manter a precisão ao longo do tempo.