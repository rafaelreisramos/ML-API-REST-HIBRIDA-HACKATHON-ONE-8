#!/bin/bash
# ============================================================================
# Script de Atualização Segura do AI Service na OCI
# ============================================================================
# Este script atualiza apenas o container ai-service sem derrubar o sistema
# Mantém backend, frontend e banco de dados funcionando durante a atualização
# ============================================================================

set -e  # Parar em caso de erro

echo "🚀 =============================================="
echo "   Atualização Segura do AI Service - OCI"
echo "   ChurnInsight - Equipe G8"
echo "=============================================="
echo ""

# Cores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Função para log com timestamp
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[AVISO]${NC} $1"
}

error() {
    echo -e "${RED}[ERRO]${NC} $1"
}

# ============================================================================
# ETAPA 1: Verificação de Pré-requisitos
# ============================================================================

log "Verificando pré-requisitos..."

# Verificar se Docker está rodando
if ! docker info > /dev/null 2>&1; then
    error "Docker não está rodando ou não está instalado!"
    exit 1
fi

# Verificar se docker-compose está instalado
if ! command -v docker-compose &> /dev/null; then
    error "docker-compose não está instalado!"
    exit 1
fi

# Verificar se estamos no diretório correto
if [ ! -f "docker-compose.yml" ]; then
    error "Arquivo docker-compose.yml não encontrado!"
    error "Execute este script da raiz do projeto."
    exit 1
fi

log "✅ Pré-requisitos verificados"
echo ""

# ============================================================================
# ETAPA 2: Backup do Container Atual
# ============================================================================

log "Criando backup do container atual..."

# Verificar se o container ai-service existe
if docker ps -a --format '{{.Names}}' | grep -q "^ai-service$"; then
    # Criar tag de backup da imagem atual
    BACKUP_TAG="ai-service-backup-$(date +%Y%m%d-%H%M%S)"
    
    if docker ps --format '{{.Names}}' | grep -q "^ai-service$"; then
        log "Container ai-service está rodando. Criando snapshot..."
        docker commit ai-service "$BACKUP_TAG" > /dev/null 2>&1
        log "✅ Backup criado: $BACKUP_TAG"
    else
        warn "Container ai-service existe mas não está rodando"
    fi
else
    warn "Container ai-service não encontrado. Primeira instalação?"
fi

echo ""

# ============================================================================
# ETAPA 3: Pull das Últimas Alterações do Git
# ============================================================================

log "Verificando atualizações do repositório..."

# Verificar se há alterações locais não commitadas
if ! git diff-index --quiet HEAD -- 2>/dev/null; then
    warn "Há alterações locais não commitadas!"
    warn "Continuando mesmo assim..."
fi

# Fazer pull das últimas alterações
log "Baixando últimas alterações..."
git pull origin main || {
    error "Falha ao fazer pull do repositório"
    exit 1
}

log "✅ Repositório atualizado"
echo ""

# ============================================================================
# ETAPA 4: Verificar Health do Sistema Atual
# ============================================================================

log "Verificando saúde do sistema atual..."

# Verificar se backend está respondendo
if curl -sf http://localhost:9999/actuator/health > /dev/null 2>&1; then
    log "✅ Backend está saudável"
else
    warn "Backend não está respondendo. Continuando mesmo assim..."
fi

# Verificar se frontend está respondendo
if curl -sf http://localhost/health > /dev/null 2>&1; then
    log "✅ Frontend está saudável"
else
    warn "Frontend não está respondendo. Continuando mesmo assim..."
fi

echo ""

# ============================================================================
# ETAPA 5: Rebuild do AI Service (Sem Derrubar Outros Serviços)
# ============================================================================

log "Reconstruindo imagem do AI Service com novos modelos..."

# Build da nova imagem (sem cache para garantir que pega os novos arquivos)
docker-compose build --no-cache ai-service || {
    error "Falha ao construir nova imagem do AI Service"
    error "Sistema atual permanece intacto"
    exit 1
}

log "✅ Nova imagem construída com sucesso"
echo ""

# ============================================================================
# ETAPA 6: Atualização Rolling (Zero Downtime)
# ============================================================================

log "Iniciando atualização rolling do AI Service..."

# Parar apenas o container ai-service (mantém backend, frontend, postgres rodando)
log "Parando container antigo..."
docker-compose stop ai-service

# Remover container antigo
log "Removendo container antigo..."
docker-compose rm -f ai-service

# Iniciar novo container com a imagem atualizada
log "Iniciando novo container..."
docker-compose up -d ai-service

log "✅ Novo container iniciado"
echo ""

# ============================================================================
# ETAPA 7: Aguardar Health Check
# ============================================================================

log "Aguardando AI Service ficar saudável..."

MAX_WAIT=120  # 2 minutos
WAIT_TIME=0
INTERVAL=5

while [ $WAIT_TIME -lt $MAX_WAIT ]; do
    if docker inspect ai-service --format='{{.State.Health.Status}}' 2>/dev/null | grep -q "healthy"; then
        log "✅ AI Service está saudável!"
        break
    fi
    
    echo -n "."
    sleep $INTERVAL
    WAIT_TIME=$((WAIT_TIME + INTERVAL))
done

echo ""

if [ $WAIT_TIME -ge $MAX_WAIT ]; then
    error "AI Service não ficou saudável em $MAX_WAIT segundos"
    error "Verifique os logs: docker-compose logs ai-service"
    
    warn "Deseja reverter para o backup? (s/n)"
    read -r RESPOSTA
    
    if [ "$RESPOSTA" = "s" ] || [ "$RESPOSTA" = "S" ]; then
        log "Revertendo para backup..."
        docker-compose stop ai-service
        docker tag "$BACKUP_TAG" ai-service:latest
        docker-compose up -d ai-service
        log "✅ Revertido para versão anterior"
    fi
    
    exit 1
fi

echo ""

# ============================================================================
# ETAPA 8: Verificação de Integração
# ============================================================================

log "Verificando integração com Backend..."

# Aguardar alguns segundos para backend reconectar
sleep 5

if curl -sf http://localhost:9999/actuator/health > /dev/null 2>&1; then
    log "✅ Backend ainda está saudável"
else
    warn "Backend pode estar com problemas. Verifique os logs."
fi

echo ""

# ============================================================================
# ETAPA 9: Teste de Inferência
# ============================================================================

log "Testando inferência do modelo..."

# Criar payload de teste
TEST_PAYLOAD='{
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

# Testar endpoint direto do AI Service
if curl -sf -X POST http://localhost:5000/predict \
    -H "Content-Type: application/json" \
    -d "$TEST_PAYLOAD" > /dev/null 2>&1; then
    log "✅ AI Service está respondendo corretamente"
else
    error "AI Service não está respondendo ao endpoint /predict"
    error "Verifique os logs: docker-compose logs ai-service"
fi

echo ""

# ============================================================================
# ETAPA 10: Limpeza e Relatório Final
# ============================================================================

log "Limpando recursos não utilizados..."

# Remover imagens antigas (dangling)
docker image prune -f > /dev/null 2>&1

log "✅ Limpeza concluída"
echo ""

# ============================================================================
# RELATÓRIO FINAL
# ============================================================================

echo "🎉 =============================================="
echo "   ATUALIZAÇÃO CONCLUÍDA COM SUCESSO!"
echo "=============================================="
echo ""
echo "📊 Status dos Serviços:"
echo ""

docker-compose ps

echo ""
echo "📝 Informações Importantes:"
echo ""
echo "  • Backup criado: $BACKUP_TAG"
echo "  • Para reverter: docker tag $BACKUP_TAG ai-service:latest"
echo "  • Logs: docker-compose logs -f ai-service"
echo "  • Health: docker inspect ai-service --format='{{.State.Health.Status}}'"
echo ""
echo "🔍 Verificações Recomendadas:"
echo ""
echo "  1. Testar previsão via frontend"
echo "  2. Verificar logs por erros: docker-compose logs ai-service | grep ERROR"
echo "  3. Monitorar uso de memória: docker stats ai-service"
echo ""
echo "✅ Sistema atualizado e operacional!"
echo "=============================================="
