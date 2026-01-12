import urllib.request
import json
import sys

BASE_URL = "http://localhost:9999"
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
            content = response.read().decode('utf-8')
            try: return json.loads(content)
            except: return content
    except urllib.error.HTTPError as e:
        print(f"❌ Erro HTTP {e.code}: {e.read().decode('utf-8')}")
        return None

def get_token():
    user_data = {"login": "test_admin_v4", "senha": "123"} # Usando o user V4 que já existe
    resp = make_request(LOGIN_URL, data=user_data)
    if resp and "token" in resp: return resp["token"]
    print("❌ Falha Login no script de teste query")
    sys.exit(1)

def test_query():
    token = get_token()
    print(f"Token obtido: {token[:10]}...")
    
    print("Testando Query Simples (Hello World do GraphQL)...")
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
    resp = make_request(GRAPHQL_URL, data=payload, token=token)
    
    if resp and "data" in resp:
        print("✅ Query de Introspecção Funcionou! Autenticação OK.")
    else:
        print("❌ Query Falhou.")

if __name__ == "__main__":
    test_query()
