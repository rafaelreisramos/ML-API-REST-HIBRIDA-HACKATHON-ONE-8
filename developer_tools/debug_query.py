import urllib.request
import json
import os
import sys

BASE_URL = os.getenv("API_URL", "http://localhost:9999")
GRAPHQL_URL = f"{BASE_URL}/graphql"
LOGIN_URL = f"{BASE_URL}/login"

def make_request(url, method="POST", data=None, token=None):
    headers = {'Content-Type': 'application/json'}
    if token:
        headers['Authorization'] = f"Bearer {token}"
    body = json.dumps(data).encode('utf-8') if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(f"Erro: {e}")
        sys.exit(1)

def get_token():
    user_data = {"login": "debug_user", "senha": "123"}
    resp = make_request(LOGIN_URL, data=user_data)
    return resp["token"]

if len(sys.argv) < 2:
    print("Uso: python debug_query.py <ID>")
    sys.exit(1)

target_id = sys.argv[1]
token = get_token()

query = """
query busca($id: ID!) {
  buscarPorId(id: $id) {
    id
    clienteId
    previsao
  }
}
"""

resp = make_request(GRAPHQL_URL, data={"query": query, "variables": {"id": target_id}}, token=token)
print(json.dumps(resp, indent=2))
