#!/usr/bin/env python3
"""
Script para testar o upload via frontend (porta 3000)
"""
import requests
import sys

# 1. Criar usuário
print("1. Criando usuário...")
create_response = requests.post(
    'http://localhost:9999/usuarios',
    json={'login': 'test_upload', 'senha': 'test123'}
)
print(f"   Status: {create_response.status_code}")
if create_response.status_code not in [200, 201]:
    print(f"   Usuário já existe ou erro: {create_response.text}")

# 2. Fazer login
print("\n2. Fazendo login...")
login_response = requests.post(
    'http://localhost:9999/login',
    json={'login': 'test_upload', 'senha': 'test123'}
)
print(f"   Status: {login_response.status_code}")

if login_response.status_code != 200:
    print(f"   ERRO no login: {login_response.text}")
    sys.exit(1)

token = login_response.json().get('token')
print(f"   Token obtido: {token[:50]}...")

# 3. Testar upload via proxy do frontend (porta 3000)
print("\n3. Testando upload via frontend (porta 3000)...")
csv_content = """cliente_id,idade,genero,tempo_assinatura_meses,plano_assinatura,valor_mensal,visualizacoes_mes,tempo_medio_sessao_min,contatos_suporte,avaliacao_conteudo_media,avaliacao_conteudo_ultimo_mes,avaliacao_plataforma,regiao
CLI-TEST,25,Masculino,12,Premium,50.0,30,60,2,4.5,4.0,4.2,Sul"""

files = {'file': ('test.csv', csv_content)}
headers = {'Authorization': f'Bearer {token}'}

upload_response = requests.post(
    'http://localhost:3000/api/churn/batch/optimized',
    files=files,
    headers=headers,
    timeout=30
)

print(f"   Status: {upload_response.status_code}")
print(f"   Headers: {upload_response.headers}")
if upload_response.status_code == 200:
    print(f"   ✅ SUCESSO! Tamanho da resposta: {len(upload_response.content)} bytes")
    # Salvar CSV de resultado
    with open('resultado_test_upload.csv', 'wb') as f:
        f.write(upload_response.content)
    print(f"   Resultado salvo em: resultado_test_upload.csv")
else:
    print(f"   ❌ ERRO: {upload_response.text[:500]}")

print(f"\n✅ Token válido para usar no frontend:")
print(f"   {token}")
