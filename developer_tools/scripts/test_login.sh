#!/bin/bash
# Script para criar usuário admin e testar login

echo "🔧 Criando usuário admin..."
curl -X POST http://localhost:9999/usuarios \
  -H "Content-Type: application/json" \
  -d '{"login":"admin","senha":"123"}'

echo -e "\n\n✅ Usuário criado! Testando login..."
curl -X POST http://localhost:9999/login \
  -H "Content-Type: application/json" \
  -d '{"login":"admin","senha":"123"}'

echo -e "\n\n🌐 Testando login via HTTPS (nip.io)..."
curl -k -X POST https://137.131.179.58.nip.io/login \
  -H "Content-Type: application/json" \
  -d '{"login":"admin","senha":"123"}'

echo -e "\n\n✅ Testes concluídos!"
