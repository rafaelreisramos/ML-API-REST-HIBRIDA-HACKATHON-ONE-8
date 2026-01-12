# Histórico de Mudanças (Changelog)

## [2026-01-11] - Consolidação e Revisão Hackathon

Hoje realizamos a revisão completa do código submetido pelos colaboradores e ajustes finos na infraestrutura.

### 🚀 Principais Alterações

* **Docker e Infraestrutura:**
  * `Dockerfile`: Adicionada variável de ambiente `JWT_TOKEN` para evitar falha na inicialização do serviço de segurança.
  * `docker-compose.yml`: Ajuste de nomes de container para evitar conflitos de porta (27017 e 5000).
  * `run_api.bat`: Script de execução atualizado para rodar de forma não-interativa (sem 'pause') e injetando o Token JWT de build.

### 🐛 Correções de Bugs (Fixes)

* **Teste E2E (`test_api_e2e.py`):**
  * Corrigido o payload da mutação GraphQL `registrarAnalise`.
  * Adicionados campos obrigatórios (`planoAssinatura`, `metodoPagamento`, `dispositivoPrincipal`, `visualizacoesMes`, `contatosSuporte`) que estavam faltando e causando erro 500 na validação do Backend.
  * Validação do teste atualizada para checar o funcionamento de ponta a ponta.

### 🛡️ Segurança e Qualidade

* Validação de que a nova camada de Services (`ChurnService`) está tratando corretamente os dados.
* Confirmação de que o `TokenService` está ativo e protegendo os endpoints (exceto GraphQL em dev).

---
*Revisado e Aprovado por: Time de Engenharia (IA + Humano)*

### Corre��es Globais de Seguran�a e Auth
- [x] Implementado cadastro de usu�rios funcional.
- [x] Corrigido erro 'Secret cannot be null' no TokenService.
- [x] Habilitado Login e Gera��o de Token JWT.
- [x] Validado fluxo E2E completo: Cadastro -> Login -> Token -> Mutation Seguro.
