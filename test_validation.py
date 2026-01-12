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
    except urllib.error.HTTPError as e:
        # GraphQL retorna 200 mesmo com erro, mas Spring Validation pode retornar 400 se configurado strict,
        # porem no spring-graphql erros de validacao costumam vir no body JSON com errors[].
        return json.loads(e.read().decode('utf-8'))
    except Exception as e:
        print(f"❌ Erro de Conexão: {e}")
        sys.exit(1)

def test_validation():
    print("🚀 Testando Validação da API (Dados Inválidos)...")
    
    # Tentando inserir idade negativa e sem nome
    mutation = """
    mutation {
      registrarAnalise(input: {
        clienteId: "",  # VAZIO (Deve falhar @NotBlank)
        idade: -5,      # NEGATIVO (Deve falhar @Min)
        genero: "",
        regiao: "Sul",
        valorMensal: -10.0,
        tempoAssinaturaMeses: 0,
        diasUltimoAcesso: 0,
        avaliacaoPlataforma: 6.0, # (Deve falhar @Max 5)
        
        # Novos campos V8 Obrigatórios
        tipoContrato: "MENSAL",
        categoriaFavorita: "GERAL",
        acessibilidade: 0,
        
        # Novos campos V4
        avaliacaoConteudoMedia: 0.0,
        avaliacaoConteudoUltimoMes: 0.0,
        tempoMedioSessaoMin: 0,
        
        previsao: "N/A",
        probabilidade: 0.0,
        riscoAlto: false
      }) {
        id
      }
    }
    """
    
    response = run_query(mutation)
    
    if "errors" in response:
        print("\n✅ API Rejeitou corretamente os dados inválidos!")
        print("Erros retornados:")
        for err in response["errors"]:
            print(f" - {err['message']}")
    else:
        print("\n❌ FALHA: A API aceitou dados inválidos! (Validação não funcionou)")
        print(json.dumps(response, indent=2))

if __name__ == "__main__":
    test_validation()
