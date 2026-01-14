#!/usr/bin/env python3
import requests

# 1. Criar usuário admin
print("1. Criando usuário admin...")
try:
    response = requests.post(
        'http://localhost:9999/usuarios',
        json={'login': 'admin', 'senha': 'admin123'}
    )
    print(f"   Status: {response.status_code}")
    print(f"   Resposta: {response.text}")
except Exception as e:
    print(f"   Erro: {e}")

# 2. Testar login
print("\n2. Testando login...")
try:
    response = requests.post(
        'http://localhost:9999/login',
        json={'login': 'admin', 'senha': 'admin123'}
    )
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Login bem-sucedido!")
        print(f"   Token: {data.get('token', 'N/A')[:50]}...")
    else:
        print(f"   ❌ Falha no login: {response.text}")
except Exception as e:
    print(f"   Erro: {e}")
