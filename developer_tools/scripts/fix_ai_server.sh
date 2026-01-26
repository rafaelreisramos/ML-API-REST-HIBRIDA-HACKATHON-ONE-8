#!/bin/bash
set -e

echo "🔧 Iniciando correção manual do AI Server..."

# 1. Instalar Docker e Dependências
echo "📦 Instalando dependências..."
sudo dnf install -y dnf-utils zip unzip git python39
sudo dnf config-manager --add-repo=https://download.docker.com/linux/centos/docker-ce.repo
sudo dnf install -y docker-ce docker-ce-cli containerd.io
sudo systemctl enable --now docker
sudo usermod -aG docker opc

# 2. Instalar Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose

# 3. Configurar Firewall (Porta 5000)
echo "🛡️ Configurando Firewall..."
sudo firewall-cmd --permanent --add-port=5000/tcp
sudo firewall-cmd --reload

# 4. Configurar AI Project
echo "🧠 Configurando AI Project..."
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

# 5. Executar Setup e Build
echo "🏗️ Construindo containers AI..."
cd ai_service
# Ajustar Dockerfile se necessário ou rodar docker-compose do AI
docker build -t churninsight-ai .
docker run -d -p 5000:5000 --name ai-service --restart unless-stopped churninsight-ai

echo "✅ AI Server corrigido! Teste interno: curl http://localhost:5000"
