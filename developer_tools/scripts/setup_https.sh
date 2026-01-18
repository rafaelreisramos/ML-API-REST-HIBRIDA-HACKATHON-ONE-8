#!/bin/bash
# Script para configurar HTTPS com Traefik e nip.io em uma instância já em execução
# Execute este script dentro da VM (via SSH)

echo "🔒 Iniciando configuração de HTTPS..."

# 1. Garantir que estamos no diretório correto
cd /opt/churninsight || exit 1

# 2. Atualizar repositório para baixar o novo docker-compose.yml
echo "⬇️ Atualizando código..."
git pull origin main

# 3. Preparar diretórios para o Traefik (Certificados)
echo "📂 Criando diretórios para certificados..."
mkdir -p ./letsencrypt
touch ./letsencrypt/acme.json
chmod 600 ./letsencrypt/acme.json

# 4. Detectar IP Público
echo "🌐 Detectando IP Público..."
PUBLIC_IP=$(curl -s ifconfig.me)

if [ -z "$PUBLIC_IP" ]; then
    echo "❌ Erro ao detectar IP Público via ifconfig.me. Tentando metadados OCI..."
    PUBLIC_IP=$(curl -s -H "Authorization: Bearer Oracle" -L http://169.254.169.254/opc/v1/instance/canonicalRegion) # Exemplo, mas ifconfig.me costuma ser suficiente
fi

if [ -z "$PUBLIC_IP" ]; then
    echo "❌ FALHA FATAL: Não foi possível determinar o IP Público."
    exit 1
fi

echo "✅ IP Detectado: $PUBLIC_IP"

# 5. Criar arquivo .env
echo "📝 Configurando variáveis de ambiente..."
echo "DOMAIN=$PUBLIC_IP.nip.io" > .env
# Manter outras variáveis se necessário, mas o docker-compose.yml já tem defaults ou usa o .env
# Se houver credenciais de banco sensíveis que não estão no docker-compose, elas deveriam estar aqui.
# Assumindo que o ambiente atual já roda, o .env vai complementar.
# Cuidado para não sobrescrever se já existir coisas importantes.
# Vamos fazer append se algo já existir, mas garantindo que DOMAIN seja atualizado.

# Melhor abordagem: Ler o .env existente, remover linha DOMAIN antiga, adicionar nova.
if [ -f .env ]; then
    sed -i '/^DOMAIN=/d' .env
fi
echo "DOMAIN=$PUBLIC_IP.nip.io" >> .env

echo "Conteúdo do .env:"
cat .env

# 6. Reiniciar containers
echo "🔄 Reiniciando containers com nova configuração..."
/usr/local/bin/docker-compose down
/usr/local/bin/docker-compose up -d --build --remove-orphans

echo "✅ Concluído!"
echo "Acesse agora: https://$PUBLIC_IP.nip.io"
