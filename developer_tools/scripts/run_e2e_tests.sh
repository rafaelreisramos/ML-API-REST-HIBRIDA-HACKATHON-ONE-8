#!/bin/bash

# Script para rodar testes E2E de forma robusta, ignorando Firewall do Windows
# Ele executa o teste DE DENTRO da rede Docker.

CONTAINER_NAME="ai-service"
BACKEND_HOST="backend-api" # Nome do serviço no docker-compose e rede interna

echo "🚀 Preparando Teste E2E (Via Docker Network)..."

# 1. Verifica se o container está rodando
if ! docker ps | grep -q "$CONTAINER_NAME"; then
    echo "❌ Erro: O container '$CONTAINER_NAME' não está rodando."
    echo "   Por favor, inicie o projeto com 'docker compose up -d' antes de testar."
    exit 1
fi

# 2. Copia o script de teste mais recente para dentro do container
echo "📦 Copiando script de teste para o container..."
docker cp test_api_e2e.py "$CONTAINER_NAME":/app/test_api_e2e.py

# 3. Executa o teste lá dentro
echo "🔥 Executando teste..."
echo "---------------------------------------------------"
docker exec -e API_URL="http://$BACKEND_HOST:9999" "$CONTAINER_NAME" python test_api_e2e.py
echo "---------------------------------------------------"
