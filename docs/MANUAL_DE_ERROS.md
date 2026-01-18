# Manual de Erros e Soluções (Troubleshooting) - ChurnInsight

Este manual reúne soluções consolidadas para problemas de configuração e execução do projeto, focado especialmente em usuários **Linux e Windows (WSL 2)**.

## 🛠️ Ferramentas de Correção Automática

Criamos scripts facilitadores na pasta `scripts/` para automatizar correções complexas:

### 1. Corrigir Ambiente Docker no WSL

Se tiver problemas de credenciais/login no Docker.

```bash
./scripts/fix_wsl_docker.sh
```

*O que faz:* Remove configurações de credenciais do Windows que quebram o Docker no Linux.

### 2. Rodar Testes Ignorando Firewall

Se tiver erros de rede (`Connection Refused`) ao rodar os testes.

```bash
./scripts/run_e2e_tests.sh
```

*O que faz:* Executa os testes de dentro da rede do Docker, sem passar pelo Firewall do Windows.

---

## 🛑 Catálogo de Erros Comuns

### 1. `docker-credential-desktop.exe: exec format error`

**Onde:** Durante o build (`docker compose up --build`).

- **Causa:** O Docker está tentando usar um executável `.exe` do Windows dentro do Linux.
- **Solução:** Execute o script `./scripts/fix_wsl_docker.sh`.

### 2. `container ai-service is unhealthy`

**Onde:** Após subir os containers.

- **Causa A:** Falta da biblioteca `requests` no container. (Corrigido na versão atual).
- **Causa B:** Timeout. O modelo de ML é grande e demora >10s para carregar.
- **Solução:** Aumentamos o `start_period` para 60s. Aguarde 1 minuto. Se persistir, veja `docker logs ai-service`.

### 3. `Address already in use` (Porta 5000, 9999 ou 80)

**Onde:** Ao iniciar `docker compose up`.

- **Causa:** Um container antigo não foi removido corretamente ou outro serviço (como Grafana ou outro app Python) está usando a porta.
- **Solução (Linux/WSL):**

  ```bash
  # Matar processo na porta 5000
  sudo fuser -k 5000/tcp
  ```

- **Solução (Geral):**

  ```bash
  # Remover todos os containers zumbis
  docker rm -f $(docker ps -aq)
  ```

### 4. `No route to host` / `Connection Refused` (Testes E2E)

**Onde:** Ao rodar `python test_api_e2e.py` no terminal WSL.

- **Causa:** O Firewall do Windows bloqueia a conexão da rede WSL para o host.
- **Solução:** Use o script `./scripts/run_e2e_tests.sh` que contorna esse problema rodando internamente.

---

## 🧹 Procedimento de Limpeza Total (Reset)

Se o ambiente estiver muito instável, realize este reset:

1. **Destruir tudo:**

   ```bash
   docker compose down -v
   docker rm -f $(docker ps -aq)
   docker system prune -a -f --volumes
   ```

2. **Corrigir Configuração:**

   ```bash
   chmod +x scripts/*.sh
   ./scripts/fix_wsl_docker.sh
   ```

3. **Reconstruir e Iniciar:**

   ```bash
   docker compose up --build -d
   ```
