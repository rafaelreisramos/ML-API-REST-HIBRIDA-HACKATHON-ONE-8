# Guia de Troubleshooting - ChurnInsight

Este documento reúne soluções para problemas comuns de configuração, instalação e execução do projeto, com foco especial em ambientes **Windows (WSL 2)**.

## 🛠️ Ferramentas de Correção Automática (Novas!)

Para facilitar sua vida, criamos scripts automáticos na pasta `scripts/`:

### 1. Corrigir Problemas de Docker no WSL

Se você receber erros como `docker-credential-desktop.exe: exec format error` ou falhas de autenticação ao subir os containers.

**Executar (no WSL):**

```bash
chmod +x scripts/fix_wsl_docker.sh
./scripts/fix_wsl_docker.sh
```

*O que ele faz:* Reseta o arquivo `~/.docker/config.json` para uma versão compatível com Linux, removendo a dependência do gerenciador de credenciais do Windows.

---

### 2. Rodar Testes E2E (Blindado contra Firewall)

Se você tentar rodar `test_api_e2e.py` e receber `Connection refused` ou `No route to host` devido ao firewall do Windows.

**Executar (no WSL):**

```bash
chmod +x scripts/run_e2e_tests.sh
./scripts/run_e2e_tests.sh
```

*O que ele faz:* Copia o teste para dentro do container `ai-service` e o executa lá dentro, onde a rede é local e não sofre bloqueios de firewall.

---

## 🛑 Erros Conhecidos e Soluções

### Erro: `docker-credentials-desktop: exec format error` ou falha no build

- **Causa:** O Docker no WSL tenta usar o executável de credenciais do Windows (`.exe`), mas não consegue rodar binários Windows nativamente durante o build.
- **Solução:** Rode o script `./scripts/fix_wsl_docker.sh` ou apague manualmente o conteúdo de `~/.docker/config.json` deixando apenas `{}`.

### Erro: `container ai-service is unhealthy`

- **Sintoma:** O comando `docker compose up` trava ou diz que o `ai-service` não está saudável.
- **Causa 1 (Biblioteca):** Falta da biblioteca `requests` ou `curl` dentro do container para rodar o healthcheck.
  - *Correção:* Certifique-se que `requests` está no `ai_service/requirements.txt` (Já corrigido na versão atual).
- **Causa 2 (Timeout):** O modelo de Machine Learning demora para carregar (>10s).
  - *Correção:* Aumentar o `start_period` no `docker-compose.yml` para `60s`.

### Erro: `Connection Refused` em `localhost:9999` (Backend)

- **Causa:** O Firewall do Windows bloqueia conexões vindas do WSL para portas mapeadas no host.
- **Solução Rápida:** Use o script `./scripts/run_e2e_tests.sh` para testar por dentro da rede Docker.
- **Solução Manual:** Tente acessar via IP do Gateway (descubra com `grep nameserver /etc/resolv.conf`) em vez de localhost.

---

## ✅ Checklist de Instalação Limpa (WSL)

Se tudo quebrar, siga este ritual de limpeza e reinstalação:

1. **Limpar Tudo:**

   ```bash
   docker rm -f $(docker ps -aq)
   docker system prune -a -f --volumes
   ```

2. **Corrigir Config:**

   ```bash
   ./scripts/fix_wsl_docker.sh
   ```

3. **Subir Aplicação:**

   ```bash
   docker compose up --build -d
   ```

4. **Verificar Logs (se falhar):**

   ```bash
   docker logs ai-service
   docker logs backend-api
   ```
