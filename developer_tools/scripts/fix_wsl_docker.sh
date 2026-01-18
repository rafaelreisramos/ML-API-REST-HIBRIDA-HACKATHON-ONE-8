#!/bin/bash

# Este script resolve o problema "docker-credential-desktop.exe: exec format error" no WSL
# e prepara o ambiente para rodar sem erros de credenciais.

echo "🔧 Diagnosticando ambiente Docker no WSL..."

DOCKER_CONFIG_FILE="$HOME/.docker/config.json"

if [ -f "$DOCKER_CONFIG_FILE" ]; then
    if grep -q "credsStore" "$DOCKER_CONFIG_FILE"; then
        echo "⚠️  Detectada configuração de credencial do Windows incompatível no Linux."
        echo "🔄 Convertendo para configuração limpa..."
        
        # Backup do original
        mv "$DOCKER_CONFIG_FILE" "$DOCKER_CONFIG_FILE.bak_$(date +%s)"
        
        # Cria novo arquivo limpo
        echo "{}" > "$DOCKER_CONFIG_FILE"
        
        echo "✅ Arquivo ~/.docker/config.json corrigido!"
        echo "   (O original foi salvo como .bak)"
    else
        echo "✅ Configuração do Docker parece OK (sem credsStore Windows)."
    fi
else
    echo "ℹ️  Nenhum arquivo de config encontrado. Criando um limpo..."
    mkdir -p "$HOME/.docker"
    echo "{}" > "$DOCKER_CONFIG_FILE"
    echo "✅ Arquivo criado."
fi

echo ""
echo "🚀 Ambiente pronto! Tente rodar 'docker compose up' agora."
