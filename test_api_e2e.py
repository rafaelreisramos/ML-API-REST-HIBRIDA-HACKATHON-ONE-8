import urllib.request
import json
import sys

import os

# Detecta URL via variável de ambiente (útil para WSL/Docker)
BASE_URL = os.getenv("API_URL", "http://localhost:9999")
print(f"📡 Usando API em: {BASE_URL}")
GRAPHQL_URL = f"{BASE_URL}/graphql"
LOGIN_URL = f"{BASE_URL}/login"
REGISTER_URL = f"{BASE_URL}/usuarios"

def make_request(url, method="POST", data=None, token=None):
    headers = {'Content-Type': 'application/json'}
    if token:
        headers['Authorization'] = f"Bearer {token}"
    
    body = json.dumps(data).encode('utf-8') if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    
    try:
        with urllib.request.urlopen(req) as response:
            if response.status == 204: return None
            content = response.read().decode('utf-8')
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                return content # Retorna texto puro se não for JSON
    except urllib.error.HTTPError as e:
        print(f"❌ Erro HTTP {e.code}: {e.read().decode('utf-8')}")
        return None
    except Exception as e:
        print(f"❌ Erro de Conexão: {e}")
        sys.exit(1)

def get_token():
    print("\n🔑 Autenticando...")
    user_data = {"login": "test_admin_v4", "senha": "123"}
    
    # 1. Tentar Cadastrar (pode falhar se já existir, tudo bem)
    make_request(REGISTER_URL, data=user_data)
    
    # 2. Tentar Logar
    resp = make_request(LOGIN_URL, data=user_data)
    if resp and "token" in resp:
        print("✅ Login realizado com sucesso!")
        return resp["token"]
    else:
        print("❌ Falha no login. Verifique o servidor.")
        sys.exit(1)

def run_graphql(query, variables=None, token=None):
    payload = {"query": query}
    if variables: payload["variables"] = variables
    return make_request(GRAPHQL_URL, data=payload, token=token)

def test_flow():
    print("🚀 Iniciando Teste E2E Seguro (Python)...")
    
    # --- Passo 0: Login ---
    token = get_token()
    
    # --- 1. Mutation: Registrar Análise ---
    print("\n1️⃣  Situação 1: Testando Mutation (registrarAnalise)...")
    mutation = """
    mutation {
      registrarAnalise(input: {
        clienteId: "TESTE-SECURE-01",
        idade: 30,
        genero: "Hibrido",
        regiao: "Nuvem",
        valorMensal: 100.00,
        tempoAssinaturaMeses: 12,
        diasUltimoAcesso: 0,
        avaliacaoPlataforma: 4.5,
        avaliacaoConteudoMedia: 4.5,
        avaliacaoConteudoUltimoMes: 4.5,
        tempoMedioSessaoMin: 60,
        planoAssinatura: "Premium",
        metodoPagamento: "Pix",
        dispositivoPrincipal: "Mobile",
        visualizacoesMes: 10,
        contatosSuporte: 0,
        tipoContrato: "MENSAL",
        categoriaFavorita: "DOCUMENTÁRIOS",
        acessibilidade: 0,
        previsao: "Analise Pendente",
        probabilidade: 0.0,
        riscoAlto: false
      }) {
        id
        clienteId
        previsao
      }
    }
    """
    
    response = run_graphql(mutation, token=token)
    
    if not response or "errors" in response:
        print("❌ Mutation Falhou!")
        if response: print(json.dumps(response, indent=2))
        sys.exit(1)
        
    created_id = response["data"]["registrarAnalise"]["id"]
    print(f"✅ Mutation Sucesso! ID Criado: {created_id}")
    
    # --- 2. Query: Buscar o dado criado ---
    print(f"\n2️⃣  Situação 2: Testando Query (buscarPorId)...")
    query = """
    query busca($id: ID!) {
      buscarPorId(id: $id) {
        id
        clienteId
        regiao
      }
    }
    """
    
    response = run_graphql(query, variables={"id": created_id}, token=token)
    
    if not response or "errors" in response:
        print("❌ Query Falhou!")
        if response: print(json.dumps(response, indent=2))
        sys.exit(1)
        
    result = response["data"]["buscarPorId"]
    print(f"✅ Query Sucesso! Cliente: {result['clienteId']}")
    print("\n✨ SUCESSO! A API está segura e funcional. ✨")

if __name__ == "__main__":
    test_flow()
