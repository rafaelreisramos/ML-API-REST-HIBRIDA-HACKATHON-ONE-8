# Histórico de Mudanças (Changelog)

## [2026-01-12] - Automação e Demonstração via Jupyter

Adicionada camada de orquestração via Notebooks para facilitar apresentações e execução "One-Click".

### ✨ Novas Funcionalidades

* **Notebooks:** `Controlador_Do_Projeto.ipynb` (infra/execução) e `Demo_Interativa_API.ipynb` (cliente).
* **Documentação:** `GUIA_RAPIDO_APRESENTACAO.md` e `MANUAL_JUPYTER.md` adicionados.

## [2026-01-11] - Consolidação e Revisão Hackathon

Revisão completa do código e ajustes na infraestrutura.

### � Melhorias e Segurança

* **Docker:** Correção JWT e portas no `docker-compose.yml`.
* **E2E:** Fix payload GraphQL e validação de campos obrigatórios.
* **Segurança:** `TokenService` validado e ativo.

### 🐛 Fixes

- [x] Cadastro e Login funcionais.
* [x] Erro 'Secret cannot be null' corrigido.
* [x] Fluxo de Mutation Seguro validado.
