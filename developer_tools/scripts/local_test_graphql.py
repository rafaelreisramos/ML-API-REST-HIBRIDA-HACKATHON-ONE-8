import urllib.request
import json
import sys
import os

# Configuração LOCAL
BASE_URL = os.getenv("API_URL", "http://localhost:9999")
print(f"📡 Testando API LOCAL: {BASE_URL}")

GRAPHQL_URL = f"{BASE_URL}/graphql"
LOGIN_URL = f"{BASE_URL}/login"

# Credenciais Confirmadas (DataInitializer.java)
CREDENCIAIS = {"login": "admin", "senha": "123456"}

def make_request(url, method="POST", data=None, token=None):
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'VibeCode-Local-Tester/1.0'
    }
    if token:
        headers['Authorization'] = f"Bearer {token}"
    
    body = json.dumps(data).encode('utf-8') if data else None
    
    try:
        req = urllib.request.Request(url, data=body, headers=headers, method=method)
        with urllib.request.urlopen(req, timeout=10) as response:
            content = response.read().decode('utf-8')
            if not content: return None
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                return content
    except urllib.error.HTTPError as e:
        try:
             error_body = e.read().decode('utf-8')
             print(f"❌ Erro HTTP {e.code}: {error_body}")
        except:
             print(f"❌ Erro HTTP {e.code}")
        return None
    except Exception as e:
        print(f"❌ Erro de Conexão: {e}")
        sys.exit(1)

def get_token():
    print(f"\n🔑 Autenticando como '{CREDENCIAIS['login']}'...")
    resp = make_request(LOGIN_URL, data=CREDENCIAIS)
    
    if resp and "token" in resp:
        print("✅ Login realizado com sucesso!")
        return resp["token"]
    else:
        print("❌ Falha no login. Verifique se o servidor está rodando e as credenciais.")
        sys.exit(1)

def test_graphql():
    token = get_token()
    
    print("\n🔍 Testando Consulta GraphQL (Introspection Check)...")
    # Query simples que não depende de dados, apenas do schema
    query = """
    query {
      __schema {
        types {
          name
        }
      }
    }
    """
    
    payload = {"query": query}
    response = make_request(GRAPHQL_URL, data=payload, token=token)
    
    if response and "data" in response:
        tipo_count = len(response["data"]["__schema"]["types"])
        print(f"✅ Sucesso! GraphQL respondeu com {tipo_count} tipos no schema.")
        print("✨ CONECTIVIDADE CONFIRMADA: Porta 9999, Login e GraphQL estão 100% funcionais.")
    else:
        print("❌ Falha na consulta GraphQL.")
        if response: print(json.dumps(response, indent=2))

if __name__ == "__main__":
    test_graphql()
