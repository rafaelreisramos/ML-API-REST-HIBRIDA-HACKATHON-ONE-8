import requests
import os
import time

# Configurações
GRAPHQL_URL = "http://localhost:9999/graphql"
TOKEN_FILE = ".token"

def carregar_token():
    # Tentar login direto
    try:
        resp = requests.post("http://localhost:9999/api/login", 
                           json={"login": "admin", "senha": "123"}) # Tentar 123 ou admin123
        if resp.status_code == 200:
            return resp.json()['token']
        
        # Tentar endpoint alternativo e senha forte
        resp = requests.post("http://localhost:9999/login", 
                           json={"login": "admin", "senha": "123"})
        if resp.status_code == 200:
            return resp.json()['token']
            
    except:
        pass
        
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'r') as f:
            print(f"✅ Token carregado do arquivo ({TOKEN_FILE})")
            return f.read().strip()
    return None

def analisar_graphql(token):
    print("🚀 Análise de Resultados - GraphQL")
    print("="*60 + "\n")

    query = """
    query {
        listarAnalises {
            clienteId
            probabilidade
            riscoAlto
            modeloUsado
            contatosSuporte
        }
    }
    """
    
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
    try:
        print("📊 Buscando resultados via GraphQL...")
        resp = requests.post(GRAPHQL_URL, json={"query": query}, headers=headers)
        
        if resp.status_code != 200:
            print(f"❌ Erro na requisição: {resp.status_code}")
            print(resp.text)
            return

        data = resp.json()
        registros = data.get('data', {}).get('listarAnalises', [])
        
        print(f"✅ {len(registros)} registros encontrados")
        print("\n" + "="*60)
        print("📈 ANÁLISE DOS RESULTADOS")
        print("="*60 + "\n")
        
        if not registros:
            print("⚠️ Nenhum registro encontrado.")
            return

        total = len(registros)
        probs = [r['probabilidade'] for r in registros]
        risco_alto = [r for r in registros if r['riscoAlto']]
        risco_medio = [r for r in registros if r['probabilidade'] >= 0.25 and not r['riscoAlto']]
        
        print(f"📊 Total de registros: {total}")
        print(f"📊 Probabilidade média: {sum(probs)/total:.2%}")
        print(f"📊 Probabilidade máxima: {max(probs):.2%}")
        print(f"📊 Probabilidade mínima: {min(probs):.2%}")
        print(f"\n🔴 Alto Risco (riscoAlto=true): {len(risco_alto)}")
        print(f"🟠 Risco Médio (prob>=25% e riscoAlto=false): {len(risco_medio)}")
        
        # Filtrar diagnósticos TEST
        diagnosticos = [r for r in registros if "TEST-" in r['clienteId']]
        if diagnosticos:
            print("\n🧐 DIAGNÓSTICO ESPECÍFICO (IDs TEST-*):")
            for r in diagnosticos:
                 print(f"  {r['clienteId']}: Prob={r['probabilidade']:.2%} | Suporte={r.get('contatosSuporte')} | Modelo={r.get('modeloUsado')}")
        else:
            print("\n⚠️ Nenhum registro TEST-* encontrado.")

    except Exception as e:
        print(f"🔥 Erro fatal: {e}")

if __name__ == "__main__":
    token = carregar_token()
    if token:
        analisar_graphql(token)
    else:
        print("❌ Token não encontrado. Faça login primeiro.")
