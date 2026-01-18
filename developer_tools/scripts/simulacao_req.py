import requests
import json
import time

BASE_URL = "http://localhost:9999"
LOGIN_URL = f"{BASE_URL}/login"
REGISTER_URL = f"{BASE_URL}/usuarios"
GRAPHQL_URL = f"{BASE_URL}/graphql"

def print_step(title):
    print(f"\n{'='*50}")
    print(f"📍 PASSO: {title}")
    print(f"{'='*50}")

def simulate():
    print("🚀 INICIANDO SIMULAÇÃO PASSO A PASSO")
    
    # 1. Autenticação
    print_step("1. AUTENTICAÇÃO (Obtendo Token)")
    credentials = {"login": "usuario_demo", "senha": "123"}
    
    # Tentar cadastrar primeiro para garantir
    print(f"🔹 Tentando cadastrar usuário: {credentials['login']}...")
    try:
        reg = requests.post(REGISTER_URL, json=credentials)
        if reg.status_code in [200, 201]:
            print("   ✅ Usuário cadastrado/verificado.")
        else:
            print(f"   ℹ️  Status cadastro: {reg.status_code} (provavelmente já existe)")
    except Exception as e:
        print(f"   ❌ Erro ao conectar no cadastro: {e}")
        return

    # Fazer Login
    print(f"🔹 Fazendo login para obter token...")
    try:
        resp = requests.post(LOGIN_URL, json=credentials)
        if resp.status_code == 200:
            token = resp.json().get("token")
            print(f"   ✅ LOGIN SUCESSO!")
            print(f"   🔑 Token JWT recebido: {token[:20]}...{token[-10:]}")
        else:
            print(f"   ❌ Falha no login: {resp.text}")
            return
    except Exception as e:
        print(f"   ❌ Erro ao conectar no login: {e}")
        return

    # 2. Preparar Dados
    print_step("2. PREPARANDO DADOS DO CLIENTE")
    # Cliente com alto risco (pouco uso, notas baixas)
    cliente_input = {
        "clienteId": "SIMULACAO-001",
        "idade": 28,
        "genero": "Masculino",
        "regiao": "Sudeste",
        "valorMensal": 29.90,
        "tempoAssinaturaMeses": 3,
        "diasUltimoAcesso": 25,          # Fator de Risco: Muito tempo sem acessar
        "avaliacaoPlataforma": 2,        # Fator de Risco: Avaliação baixa
        "avaliacaoConteudoMedia": 2.5,
        "avaliacaoConteudoUltimoMes": 1, # Fator de Risco: Insatisfação recente
        "tempoMedioSessaoMin": 5,        # Fator de Risco: Sessões curtas
        "planoAssinatura": "Basico",
        "metodoPagamento": "Cartao",
        "dispositivoPrincipal": "Mobile",
        "visualizacoesMes": 2,           # Fator de Risco: Pouco uso
        "contatosSuporte": 3,
        "tipoContrato": "MENSAL",
        "categoriaFavorita": "ESPORTES",
        "acessibilidade": 0,
        "previsao": "Pendente",
        "probabilidade": 0.0,
        "riscoAlto": False
    }
    
    print("🔹 Dados do cliente para análise:")
    print(json.dumps(cliente_input, indent=2))

    # 3. Executar Requisição GraphQL
    print_step("3. ENVIANDO REQUISIÇÃO (GraphQL Mutation)")
    
    mutation = """
    mutation registrar($input: ChurnInput!) {
      registrarAnalise(input: $input) {
        id
        clienteId
        previsao
        probabilidade
        riscoAlto
      }
    }
    """
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    payload = {
        "query": mutation,
        "variables": {"input": cliente_input}
    }
    
    print(f"🔹 Enviando POST para {GRAPHQL_URL}...")
    try:
        start_time = time.time()
        api_resp = requests.post(GRAPHQL_URL, json=payload, headers=headers)
        duration = time.time() - start_time
        
        print(f"   ⏱️  Tempo de resposta: {duration:.3f}s")
        
        if api_resp.status_code == 200:
            print("   ✅ Resposta recebida da API!")
            result = api_resp.json()
            
            if "errors" in result:
                print("   ❌ Erro retornado pelo GraphQL:")
                print(json.dumps(result["errors"], indent=2))
            else:
                data = result["data"]["registrarAnalise"]
                print_step("4. RESULTADO DA ANÁLISE")
                print("🔹 IA processou os dados:")
                print(f"   🆔 ID Gerado: {data['id']}")
                print(f"   👤 Cliente: {data['clienteId']}")
                print(f"   🎲 Probabilidade Churn: {data['probabilidade']:.1f}%")
                print(f"   📊 Previsão: {data['previsao']}")
                print(f"   ⚠️ Risco Alto? {'SIM 🔴' if data['riscoAlto'] else 'NÃO 🟢'}")
                
        else:
            print(f"   ❌ Erro HTTP {api_resp.status_code}: {api_resp.text}")

    except Exception as e:
        print(f"   ❌ Erro na requisição: {e}")

if __name__ == "__main__":
    simulate()
