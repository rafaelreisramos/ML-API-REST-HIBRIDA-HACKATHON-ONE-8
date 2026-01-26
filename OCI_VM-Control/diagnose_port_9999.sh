#!/bin/bash
# ============================================================================
# DIAGNÓSTICO DE CONECTIVIDADE - PORTA 9999 (GraphQL)
# ============================================================================
# Script para identificar por que http://IP:9999/graphql não é acessível
# ============================================================================

echo "============================================================================"
echo "  DIAGNÓSTICO DE CONECTIVIDADE - PORTA 9999"
echo "============================================================================"
echo ""

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ============================================================================
# TESTE 1: Verificar se a aplicação está rodando
# ============================================================================
echo -e "${BLUE}[TESTE 1]${NC} Verificando se a aplicação está rodando..."
if docker ps | grep -q "backend"; then
    echo -e "${GREEN}✓ Container backend está RODANDO${NC}"
    docker ps | grep backend
else
    echo -e "${RED}✗ Container backend NÃO está rodando${NC}"
    echo "  Sugestão: Execute 'docker-compose up -d' no diretório da aplicação"
fi
echo ""

# ============================================================================
# TESTE 2: Verificar em qual interface a porta 9999 está escutando
# ============================================================================
echo -e "${BLUE}[TESTE 2]${NC} Verificando em qual interface a porta 9999 está escutando..."
LISTEN_CHECK=$(sudo netstat -tulpn 2>/dev/null | grep :9999 || sudo ss -tulpn 2>/dev/null | grep :9999)

if [ -z "$LISTEN_CHECK" ]; then
    echo -e "${RED}✗ NENHUM processo está escutando na porta 9999${NC}"
    echo "  Problema: A aplicação não está rodando ou não está na porta 9999"
else
    echo "$LISTEN_CHECK"
    
    if echo "$LISTEN_CHECK" | grep -q "0.0.0.0:9999\|:::9999"; then
        echo -e "${GREEN}✓ Aplicação está escutando em TODAS as interfaces (0.0.0.0)${NC}"
        echo "  Isso está CORRETO para acesso externo"
    elif echo "$LISTEN_CHECK" | grep -q "127.0.0.1:9999"; then
        echo -e "${RED}✗ Aplicação está escutando APENAS em localhost (127.0.0.1)${NC}"
        echo "  Problema: Aplicação não aceita conexões externas"
        echo "  Solução: Configurar server.address=0.0.0.0 no application.properties"
    fi
fi
echo ""

# ============================================================================
# TESTE 3: Verificar regras do firewall
# ============================================================================
echo -e "${BLUE}[TESTE 3]${NC} Verificando regras do firewall (firewalld)..."
if systemctl is-active --quiet firewalld; then
    echo -e "${YELLOW}⚠ Firewalld está ATIVO${NC}"
    
    if sudo firewall-cmd --list-ports 2>/dev/null | grep -q "9999/tcp"; then
        echo -e "${GREEN}✓ Porta 9999/tcp está LIBERADA no firewall${NC}"
    else
        echo -e "${RED}✗ Porta 9999/tcp NÃO está liberada no firewall${NC}"
        echo "  Problema: Firewall está bloqueando conexões externas"
        echo "  Solução:"
        echo "    sudo firewall-cmd --permanent --add-port=9999/tcp"
        echo "    sudo firewall-cmd --reload"
    fi
    
    echo ""
    echo "Portas atualmente liberadas:"
    sudo firewall-cmd --list-ports 2>/dev/null || echo "  Nenhuma porta customizada"
else
    echo -e "${GREEN}✓ Firewalld está INATIVO (não está bloqueando)${NC}"
fi
echo ""

# ============================================================================
# TESTE 4: Testar conectividade local
# ============================================================================
echo -e "${BLUE}[TESTE 4]${NC} Testando conectividade LOCAL (dentro da VM)..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:9999/actuator/health 2>/dev/null || echo "000")

if [ "$HTTP_CODE" = "200" ]; then
    echo -e "${GREEN}✓ Aplicação responde localmente (HTTP $HTTP_CODE)${NC}"
    echo "  Endpoint testado: http://localhost:9999/actuator/health"
elif [ "$HTTP_CODE" = "000" ]; then
    echo -e "${RED}✗ Não foi possível conectar localmente${NC}"
    echo "  Problema: Aplicação não está respondendo"
else
    echo -e "${YELLOW}⚠ Aplicação responde com HTTP $HTTP_CODE${NC}"
    echo "  Pode ser normal se o endpoint requer autenticação"
fi
echo ""

# ============================================================================
# TESTE 5: Testar endpoint GraphQL localmente
# ============================================================================
echo -e "${BLUE}[TESTE 5]${NC} Testando endpoint GraphQL localmente..."
GRAPHQL_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:9999/graphql 2>/dev/null || echo "000")

if [ "$GRAPHQL_CODE" = "200" ]; then
    echo -e "${GREEN}✓ GraphQL responde com HTTP 200${NC}"
elif [ "$GRAPHQL_CODE" = "401" ] || [ "$GRAPHQL_CODE" = "403" ]; then
    echo -e "${YELLOW}⚠ GraphQL responde com HTTP $GRAPHQL_CODE (Autenticação requerida)${NC}"
    echo "  Isso é NORMAL - GraphQL requer token JWT"
    echo "  Para acessar:"
    echo "    1. Fazer login em /login para obter token"
    echo "    2. Usar: Authorization: Bearer <TOKEN>"
elif [ "$GRAPHQL_CODE" = "000" ]; then
    echo -e "${RED}✗ Não foi possível conectar ao GraphQL${NC}"
else
    echo -e "${YELLOW}⚠ GraphQL responde com HTTP $GRAPHQL_CODE${NC}"
fi
echo ""

# ============================================================================
# TESTE 6: Verificar IP público da VM
# ============================================================================
echo -e "${BLUE}[TESTE 6]${NC} Verificando IP público da VM..."
PUBLIC_IP=$(curl -s ifconfig.me 2>/dev/null || curl -s icanhazip.com 2>/dev/null || echo "Não detectado")
echo "  IP Público: $PUBLIC_IP"
echo ""

# ============================================================================
# TESTE 7: Testar conectividade externa (da própria VM)
# ============================================================================
echo -e "${BLUE}[TESTE 7]${NC} Testando conectividade EXTERNA (VM -> IP Público)..."
if [ "$PUBLIC_IP" != "Não detectado" ]; then
    EXT_CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 http://$PUBLIC_IP:9999/actuator/health 2>/dev/null || echo "000")
    
    if [ "$EXT_CODE" = "200" ]; then
        echo -e "${GREEN}✓ Aplicação é acessível externamente via IP público${NC}"
    elif [ "$EXT_CODE" = "000" ]; then
        echo -e "${RED}✗ Não foi possível conectar via IP público${NC}"
        echo "  Problema: Firewall ou Security List bloqueando"
    else
        echo -e "${YELLOW}⚠ Resposta HTTP $EXT_CODE via IP público${NC}"
    fi
else
    echo -e "${YELLOW}⚠ Não foi possível detectar IP público${NC}"
fi
echo ""

# ============================================================================
# RESUMO E RECOMENDAÇÕES
# ============================================================================
echo "============================================================================"
echo -e "${BLUE}  RESUMO E PRÓXIMOS PASSOS${NC}"
echo "============================================================================"
echo ""

# Análise inteligente
ISSUES_FOUND=0

if ! docker ps | grep -q "backend"; then
    echo -e "${RED}[CRÍTICO]${NC} Container backend não está rodando"
    echo "  → Execute: cd /caminho/do/projeto && docker-compose up -d"
    ISSUES_FOUND=$((ISSUES_FOUND + 1))
fi

if [ -n "$LISTEN_CHECK" ] && echo "$LISTEN_CHECK" | grep -q "127.0.0.1:9999"; then
    echo -e "${RED}[CRÍTICO]${NC} Aplicação escutando apenas em localhost"
    echo "  → Adicione 'server.address=0.0.0.0' no application.properties"
    ISSUES_FOUND=$((ISSUES_FOUND + 1))
fi

if systemctl is-active --quiet firewalld; then
    if ! sudo firewall-cmd --list-ports 2>/dev/null | grep -q "9999/tcp"; then
        echo -e "${RED}[CRÍTICO]${NC} Porta 9999 bloqueada pelo firewall"
        echo "  → Execute:"
        echo "    sudo firewall-cmd --permanent --add-port=9999/tcp"
        echo "    sudo firewall-cmd --reload"
        ISSUES_FOUND=$((ISSUES_FOUND + 1))
    fi
fi

if [ $ISSUES_FOUND -eq 0 ]; then
    echo -e "${GREEN}✓ Nenhum problema crítico detectado!${NC}"
    echo ""
    echo "Se ainda não consegue acessar externamente:"
    echo "  1. Verifique Security List na OCI Console"
    echo "  2. Teste com: curl http://$PUBLIC_IP:9999/actuator/health"
    echo "  3. Para GraphQL, use autenticação JWT"
else
    echo ""
    echo -e "${YELLOW}Total de problemas encontrados: $ISSUES_FOUND${NC}"
fi

echo ""
echo "============================================================================"
echo "  URL para teste externo: http://$PUBLIC_IP:9999/graphql"
echo "============================================================================"
