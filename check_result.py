import requests

LOGIN_URL = "http://localhost:9999/login"
GRAPHQL_URL = "http://localhost:9999/graphql"

def check():
    print("🔑 Autenticando...")
    try:
        auth = requests.post(LOGIN_URL, json={"login": "admin", "senha": "123"})
        if auth.status_code != 200:
            # Tenta com o user de teste caso admin nao exista
            auth = requests.post(LOGIN_URL, json={"login": "user_50k", "senha": "123"})
            
        token = auth.json().get("token")
        headers = {"Authorization": f"Bearer {token}"}
        
        # Query com campos em PT-BR (provável schema)
        query = """
        query {
            listarAnalises {
                clienteId
                valorMensal
                previsao
                probabilidade
                riscoAlto
            }
        }
        """
        
        print("🔍 Buscando todos os clientes e resultados...")
        resp = requests.post(GRAPHQL_URL, json={"query": query}, headers=headers)
        
        if resp.status_code == 200:
            data = resp.json().get("data", {}).get("listarAnalises", [])
            print(f"✅ Total recuperado: {len(data)}")
            
            # Salvar em arquivo
            import json
            output_file = "dump_banco_50k.json"
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            
            print(f"💾 Arquivo salvo com sucesso: {output_file}")
            
            print("🔍 Primeiros 3 registros do JSON:")
            print(json.dumps(data[:3], indent=2))
            
        else:
            print(f"❌ Erro: {resp.text}")

    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    check()
