import urllib.request
import json
import sys

URL = "http://localhost:9999/graphql"

def run_query(query, variables=None):
    payload = {"query": query}
    if variables:
        payload["variables"] = variables
    
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(URL, data=data, headers={'Content-Type': 'application/json'})
    
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(f"❌ Erro de Conexão: {e}")
        print("Certifique-se que o servidor está rodando na porta 9999.")
        sys.exit(1)

def test_flow():
    print("🚀 Iniciando Teste E2E (Script Python Automation)...")
    print(f"📡 Target: {URL}\n")
    
    # --- 1. Mutation: Registrar Análise ---
    print("1️⃣  Situação 1: Testando Mutation (registrarAnalise)...")
    mutation = """
    mutation {
      registrarAnalise(input: {
        clienteId: "TESTE-E2E-AUTO",
        idade: 99,
        genero: "Robo",
        regiao: "Cyberspace",
        valorMensal: 999.99,
        tempoAssinaturaMeses: 1,
        diasUltimoAcesso: 0,
        avaliacaoPlataforma: 5.0,
        avaliacaoConteudoMedia: 5.0,
        avaliacaoConteudoUltimoMes: 5.0,
        tempoMedioSessaoMin: 120,
        planoAssinatura: "Premium",
        metodoPagamento: "Credito",
        dispositivoPrincipal: "Desktop",
        visualizacoesMes: 50,
        contatosSuporte: 1,
        previsao: "Fiel",
        probabilidade: 0.00,
        riscoAlto: false
      }) {
        id
        clienteId
        previsao
      }
    }
    """
    
    response = run_query(mutation)
    
    if "errors" in response:
        print("❌ Mutation Falhou!")
        print(json.dumps(response, indent=2))
        sys.exit(1)
        
    created_id = response["data"]["registrarAnalise"]["id"]
    print(f"✅ Mutation Sucesso! ID Criado: {created_id}")
    
    # --- 2. Query: Buscar o dado criado ---
    print(f"\n2️⃣  Situação 2: Testando Query (buscarPorId) para o ID: {created_id}...")
    query = """
    query busca($id: ID!) {
      buscarPorId(id: $id) {
        id
        clienteId
        regiao
        valorMensal
        previsao
      }
    }
    """
    
    response = run_query(query, variables={"id": created_id})
    
    if "errors" in response:
        print("❌ Query Falhou!")
        print(json.dumps(response, indent=2))
        sys.exit(1)
        
    result = response["data"]["buscarPorId"]
    
    # --- 3. Validação ---
    print("\n🔍 Validando Dados Retornados:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    if result["clienteId"] == "TESTE-E2E-AUTO" and result["regiao"] == "Cyberspace":
         print("\n✨ SUCESSO! O teste de ponta a ponta passou. A API está Gravando e Lendo corretamente. ✨")
    else:
         print("\n⚠️  Alerta: Os dados retornados não conferem com o esperado.")

if __name__ == "__main__":
    test_flow()
