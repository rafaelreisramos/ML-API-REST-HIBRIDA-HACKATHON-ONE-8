# 🔄 Guia de Atualização Segura do AI Service na OCI

## 📋 Visão Geral

Este guia descreve como atualizar o serviço de IA (AI Service) na máquina OCI **sem causar downtime** ou afetar o funcionamento do backend, frontend e banco de dados.

---

## 🎯 Objetivo

Atualizar os modelos de Machine Learning (`.joblib`) no container `ai-service` que está rodando na OCI, garantindo:

- ✅ **Zero Downtime**: Backend e Frontend continuam funcionando
- ✅ **Backup Automático**: Versão anterior é preservada
- ✅ **Rollback Rápido**: Possibilidade de reverter em caso de problemas
- ✅ **Health Checks**: Validação automática após atualização

---

## 🛠️ Ferramentas Criadas

### 1. `update_ai_service_safe.sh` (Script Bash)

- Executa na VM OCI
- Faz backup do container atual
- Reconstrói apenas o ai-service
- Valida saúde do sistema
- Permite rollback automático

### 2. `update_ai_service_remote.ps1` (Script PowerShell)

- Executa no seu Windows local
- Conecta via SSH na OCI
- Transfere e executa o script bash
- Monitora a atualização remotamente

---

## 📝 Pré-requisitos

Antes de executar a atualização, certifique-se de que:

1. ✅ **Git está atualizado localmente**

   ```powershell
   git status
   git pull origin main
   ```

2. ✅ **Modelos foram commitados e pushed**

   ```powershell
   git log --oneline -1
   # Deve mostrar: "feat: Sincronizar modelos ML..."
   ```

3. ✅ **Arquivo `config.bat` está configurado**
   - Localização: `OCI_VM-Control/config.bat`
   - Deve conter: `INSTANCE_OCID`, `SSH_KEY_PATH`, `SSH_USER`

4. ✅ **VM OCI está rodando**

   ```powershell
   cd OCI_VM-Control
   .\CONTROLE_OCI.bat
   # Opção 3: Health Check
   ```

---

## 🚀 Método 1: Atualização Remota (Recomendado)

Execute do seu computador Windows, sem precisar conectar manualmente na VM.

### Passo 1: Navegar até o diretório

```powershell
cd d:\Alura_HACKA\ML-API-REST-HIBRIDA-HACKATHON-ONE-8\OCI_VM-Control
```

### Passo 2: Executar script de atualização remota

```powershell
.\update_ai_service_remote.ps1
```

### Passo 3: Acompanhar execução

O script irá:

1. Conectar via SSH na VM
2. Transferir o script de atualização
3. Executar a atualização
4. Mostrar logs em tempo real
5. Validar saúde do sistema

### Passo 4: Verificar resultado

Ao final, você verá:

```
🎉 ==============================================
   ATUALIZAÇÃO REMOTA CONCLUÍDA!
==============================================

✅ Sistema atualizado e operacional na OCI!
```

---

## 🔧 Método 2: Atualização Manual via SSH

Se preferir ter controle total, conecte manualmente na VM.

### Passo 1: Conectar na VM

```powershell
cd OCI_VM-Control
.\CONTROLE_OCI.bat
# Opção 4: Auto SSH
```

### Passo 2: Navegar até o projeto

```bash
cd ~/ML-API-REST-HIBRIDA-HACKATHON-ONE-8
```

### Passo 3: Atualizar código do repositório

```bash
git pull origin main
```

### Passo 4: Executar script de atualização

```bash
# Baixar script (se não estiver presente)
curl -O https://raw.githubusercontent.com/Araken13/ML-API-REST-HIBRIDA-HACKATHON-ONE-8/main/OCI_VM-Control/update_ai_service_safe.sh

# Dar permissão de execução
chmod +x update_ai_service_safe.sh

# Executar
./update_ai_service_safe.sh
```

### Passo 5: Acompanhar logs

```bash
# Em outro terminal SSH
docker-compose logs -f ai-service
```

---

## 📊 O Que Acontece Durante a Atualização

### Timeline da Atualização

```
┌─────────────────────────────────────────────────────────┐
│ 1. Verificação de Pré-requisitos (5s)                  │
│    ✓ Docker rodando                                     │
│    ✓ docker-compose instalado                           │
│    ✓ Arquivo docker-compose.yml presente                │
├─────────────────────────────────────────────────────────┤
│ 2. Backup do Container Atual (10s)                     │
│    ✓ Snapshot do container ai-service                   │
│    ✓ Tag: ai-service-backup-YYYYMMDD-HHMMSS            │
├─────────────────────────────────────────────────────────┤
│ 3. Pull do Repositório (15s)                           │
│    ✓ git pull origin main                               │
│    ✓ Novos modelos .joblib baixados                     │
├─────────────────────────────────────────────────────────┤
│ 4. Health Check do Sistema (5s)                        │
│    ✓ Backend: http://localhost:9999/actuator/health    │
│    ✓ Frontend: http://localhost/health                  │
├─────────────────────────────────────────────────────────┤
│ 5. Rebuild da Imagem (60-90s)                          │
│    ✓ docker-compose build --no-cache ai-service        │
│    ✓ Copia novos modelos do hackathon_g8_one/          │
├─────────────────────────────────────────────────────────┤
│ 6. Atualização Rolling (20s)                           │
│    ✓ docker-compose stop ai-service                     │
│    ✓ docker-compose rm -f ai-service                    │
│    ✓ docker-compose up -d ai-service                    │
│    ⚠️ Backend/Frontend/Postgres CONTINUAM RODANDO       │
├─────────────────────────────────────────────────────────┤
│ 7. Aguardar Health Check (30-60s)                      │
│    ✓ Espera container ficar "healthy"                   │
│    ✓ Timeout: 120 segundos                              │
├─────────────────────────────────────────────────────────┤
│ 8. Verificação de Integração (10s)                     │
│    ✓ Backend ainda está saudável                        │
│    ✓ Teste de inferência no AI Service                  │
├─────────────────────────────────────────────────────────┤
│ 9. Limpeza (5s)                                         │
│    ✓ Remove imagens antigas (dangling)                  │
└─────────────────────────────────────────────────────────┘

⏱️ Tempo Total: ~3-5 minutos
```

---

## 🔍 Verificações Pós-Atualização

### 1. Verificar Status dos Containers

```bash
docker-compose ps
```

Esperado:

```
NAME            STATE    PORTS
ai-service      Up       0.0.0.0:5000->5000/tcp (healthy)
backend-api     Up       0.0.0.0:9999->9999/tcp (healthy)
frontend-ui     Up       80/tcp
churn-postgres  Up       0.0.0.0:5432->5432/tcp (healthy)
```

### 2. Verificar Logs do AI Service

```bash
docker-compose logs --tail=50 ai-service
```

Procure por:

```
✅ [AI SERVICE] Modelo G8 carregado com SUCESSO.
✅ [AI SERVICE] Threshold carregado: 0.4287059456550982
✅ [AI SERVICE] RFE Selector carregado.
```

### 3. Testar Endpoint de Inferência

```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "idade": 30,
    "tempoAssinaturaMeses": 12,
    "planoAssinatura": "Premium",
    "valorMensal": 89.90,
    "visualizacoesMes": 50,
    "contatosSuporte": 1,
    "metodoPagamento": "Credito",
    "dispositivoPrincipal": "Mobile",
    "avaliacaoConteudoMedia": 4.5,
    "avaliacaoConteudoUltimoMes": 4.0,
    "tempoMedioSessaoMin": 60,
    "diasUltimoAcesso": 2,
    "avaliacaoPlataforma": 4.5,
    "regiao": "Sudeste",
    "genero": "Masculino",
    "tipoContrato": "ANUAL",
    "categoriaFavorita": "FILMES",
    "acessibilidade": 0
  }'
```

Resposta esperada:

```json
{
  "previsao": "Vai continuar",
  "probabilidade": 0.1234,
  "riscoAlto": false,
  "modeloUsado": "RandomForest G8 (Threshold: 0.4287059456550982)"
}
```

### 4. Testar via Frontend

1. Acesse: `http://<IP_OCI>` ou `https://<IP_OCI>.nip.io`
2. Faça login
3. Teste uma previsão individual
4. Verifique o dashboard de analytics

---

## 🆘 Troubleshooting

### Problema: AI Service não fica "healthy"

**Sintomas:**

```
❌ AI Service não ficou saudável em 120 segundos
```

**Diagnóstico:**

```bash
docker-compose logs ai-service
```

**Causas Comuns:**

1. Modelos `.joblib` não foram copiados corretamente
2. Erro de memória (modelos são grandes)
3. Dependências Python faltando

**Solução:**

```bash
# Verificar se modelos existem no container
docker exec ai-service ls -lh /app/models/

# Deve mostrar:
# modelo_churn.joblib (29.7 MB)
# rfe_selector.joblib (4.0 MB)
```

---

### Problema: Backend perdeu conexão com AI Service

**Sintomas:**

```
Backend retorna erro 500 ao fazer previsão
```

**Diagnóstico:**

```bash
docker-compose logs backend | grep "ai-service"
```

**Solução:**

```bash
# Reiniciar backend para reconectar
docker-compose restart backend
```

---

### Problema: Preciso reverter para versão anterior

**Solução Rápida:**

```bash
# Listar backups disponíveis
docker images | grep ai-service-backup

# Reverter para backup específico
docker-compose stop ai-service
docker tag ai-service-backup-20260121-215700 ai-service:latest
docker-compose up -d ai-service
```

---

## 📈 Monitoramento Contínuo

### Verificar Uso de Recursos

```bash
docker stats ai-service
```

### Monitorar Logs em Tempo Real

```bash
docker-compose logs -f ai-service
```

### Verificar Health Status

```bash
docker inspect ai-service --format='{{.State.Health.Status}}'
```

---

## ✅ Checklist de Atualização

Antes de executar:

- [ ] Código commitado e pushed para `origin/main`
- [ ] Modelos `.joblib` presentes em `hackathon_g8_one/models/`
- [ ] VM OCI está rodando
- [ ] `config.bat` configurado corretamente
- [ ] Backup manual feito (opcional, mas recomendado)

Durante a execução:

- [ ] Script executou sem erros
- [ ] AI Service ficou "healthy"
- [ ] Backend continua respondendo
- [ ] Frontend continua acessível

Após a atualização:

- [ ] Teste de inferência passou
- [ ] Logs não mostram erros
- [ ] Dashboard analytics funciona
- [ ] Batch upload funciona

---

## 🎯 Resumo

**Comando Único para Atualização:**

```powershell
cd OCI_VM-Control
.\update_ai_service_remote.ps1
```

**Tempo Estimado:** 3-5 minutos  
**Downtime:** Zero (outros serviços continuam rodando)  
**Rollback:** Automático em caso de falha

---

**Última Atualização:** 21/01/2026  
**Versão:** 1.0  
**Equipe:** G8 - ChurnInsight
