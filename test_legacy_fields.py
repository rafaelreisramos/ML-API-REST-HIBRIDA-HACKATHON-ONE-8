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
        return {}

def test_legacy_fields():
    print("🚀 Testando Campos Legados (Migração Python -> Java)...")
    
    mutation = """
    mutation {
      registrarAnalise(input: {
        clienteId: "MIGRACAO-001",
        idade: 35,
        genero: "Masculino",
        regiao: "Norte",
        valorMensal: 45.90,
        tempoAssinaturaMeses: 24,
        diasUltimoAcesso: 1,
        
        # --- CAMPOS LEGADOS (PYTHON) ---
        planoAssinatura: "Premium",
        metodoPagamento: "Pix",
        dispositivoPrincipal: "Smart TV",
        visualizacoesMes: 50,
        contatosSuporte: 0,
        
        # Novos campos V8
        tipoContrato: "MENSAL",
        categoriaFavorita: "FILMES",
        acessibilidade: 0,
        
        # -------------------------------
        
        avaliacaoPlataforma: 4.5,
        avaliacaoConteudoMedia: 4.5,
        avaliacaoConteudoUltimoMes: 5.0,
        tempoMedioSessaoMin: 45,
        
        previsao: "Vai continuar",
        probabilidade: 0.1,
        riscoAlto: false
      }) {
        id
        clienteId
        planoAssinatura
        metodoPagamento
        dispositivoPrincipal
        visualizacoesMes
        modeloUsado
      }
    }
    """
    
    response = run_query(mutation)
    
    if "errors" in response:
        print("❌ FALHA: A API rejeitou os novos campos!")
        print(json.dumps(response, indent=2))
        sys.exit(1)
        
    data = response.get("data", {}).get("registrarAnalise", {})
    if data.get("planoAssinatura") == "Premium":
        print("✅ SUCESSO! Campos legados aceitos e salvos corretamente.")
        print(f"🧠 Modelo Usado: {data.get('modeloUsado')}")
        print(json.dumps(data, indent=2))
    else:
        print("⚠️ ALERTA: Retorno inesperado.")
        print(json.dumps(response, indent=2))

if __name__ == "__main__":
    test_legacy_fields()
