#!/bin/bash
set -e

echo "🔧 Iniciando correção manual do App Server..."

# 1. Instalar Docker e Git
echo "📦 Instalando dependências..."
sudo dnf install -y dnf-utils zip unzip git
sudo dnf config-manager --add-repo=https://download.docker.com/linux/centos/docker-ce.repo
sudo dnf install -y docker-ce docker-ce-cli containerd.io
sudo systemctl enable --now docker

# Adicionar usuário ao grupo docker
sudo usermod -aG docker opc

# 2. Instalar Docker Compose
echo "📦 Instalando Docker Compose..."
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose

# 3. Configurar Firewall
echo "🛡️ Configurando Firewall..."
sudo firewall-cmd --permanent --add-port=80/tcp
sudo firewall-cmd --permanent --add-port=443/tcp
sudo firewall-cmd --permanent --add-port=9999/tcp
sudo firewall-cmd --reload

# 4. Configurar App
echo "🚀 Configurando Aplicação..."
sudo mkdir -p /opt/churninsight
sudo chown -R opc:opc /opt/churninsight
cd /opt/churninsight

if [ -d ".git" ]; then
    echo "Atualizando repositório..."
    git pull origin main
else
    echo "Clonando repositório..."
    git clone https://github.com/Araken13/ML-API-REST-HIBRIDA-HACKATHON-ONE-8.git .
fi

# 5. Build e Run
echo "🏗️ Construindo containers..."
sudo /usr/local/bin/docker-compose -f docker-compose.prod.yml down || true
sudo /usr/local/bin/docker-compose -f docker-compose.prod.yml up -d --build

echo "✅ Correção concluída! Acesse http://$(curl -s ifconfig.me)"
