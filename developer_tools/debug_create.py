import urllib.request
import json
import os
import sys

BASE_URL = os.getenv("API_URL", "http://localhost:9999")
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
            return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(f"Erro: {e}")
        sys.exit(1)

def get_token():
    user_data = {"login": "debug_user", "senha": "123"}
    try: make_request(REGISTER_URL, data=user_data) 
    except: pass
    resp = make_request(LOGIN_URL, data=user_data)
    return resp["token"]

mutation = """
mutation {
  registrarAnalise(input: {
    clienteId: "DEBUG-01", idade: 25, genero: "M", regiao: "Sul", valorMensal: 50.0,
    tempoAssinaturaMeses: 6, diasUltimoAcesso: 1, avaliacaoPlataforma: 5.0,
    avaliacaoConteudoMedia: 4.0, avaliacaoConteudoUltimoMes: 4.0, tempoMedioSessaoMin: 30,
    planoAssinatura: "Basico", metodoPagamento: "Credito", dispositivoPrincipal: "Mobile",
    visualizacoesMes: 5, contatosSuporte: 0, tipoContrato: "MENSAL", categoriaFavorita: "FILMES",
    acessibilidade: 0, previsao: "Pendente", probabilidade: 0.0, riscoAlto: false
  }) { id clienteId }
}
"""

token = get_token()
print(f"Token obtido.")
resp = make_request(GRAPHQL_URL, data={"query": mutation}, token=token)
if "errors" in resp:
    print(json.dumps(resp, indent=2))
else:
    id_criado = resp["data"]["registrarAnalise"]["id"]
    print(f"CRIADO_ID:{id_criado}")
