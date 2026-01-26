import requests
import json
import time
import os
import sys

# Configuração Centralizada
BASE_URL = os.getenv("API_URL", "http://localhost:9999")
LOGIN_URL = f"{BASE_URL}/login"
BATCH_URL = f"{BASE_URL}/api/churn/batch/optimized"
INPUT_PREFIX = "teste_batch" 
INPUT_PREFIX = "teste_batch" 
INPUT_FILE = "teste_batch_100.csv"

def create_dummy_csv(filename):
    print(f"⚠️ Criando arquivo de teste {filename}...")
    header = "clienteId,idade,genero,regiao,valorMensal,tempoAssinaturaMeses,diasUltimoAcesso,avaliacaoPlataforma,avaliacaoConteudoMedia,avaliacaoConteudoUltimoMes,tempoMedioSessaoMin,planoAssinatura,metodoPagamento,dispositivoPrincipal,visualizacoesMes,contatosSuporte,tipoContrato,categoriaFavorita,acessibilidade"
    
    # Criar 50 linhas de dados fake
    rows = [header]
    for i in range(50):
        rows.append(f"BATCH-{i},30,Masculino,Sudeste,50.0,12,2,4.5,4.0,4.2,45,Premium,CreditCard,Mobile,20,1,MENSAL,ACAO,0")
        
    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(rows))
    print("✅ Arquivo criado.")

# Garante que o arquivo existe
if not os.path.exists(INPUT_FILE):
    create_dummy_csv(INPUT_FILE)


def get_token():
    """Autentica com credenciais admin e retorna o token JWT"""
    print(f"🔑 Autenticando em {LOGIN_URL}...")
    user_data = {"login": "admin", "senha": "123456"}
    
    try:
        response = requests.post(LOGIN_URL, json=user_data)
        if response.status_code == 200:
            token = response.json().get("token")
            print("✅ Login realizado com sucesso!")
            return token
        elif response.status_code == 403: # Caso usuário admin não exista ou senha errada
            # Fallback para usuário de teste
            print("⚠️ Admin falhou, tentando test_user...")
            user_data = {"login": "test_batch_user", "senha": "123"}
            requests.post(f"{BASE_URL}/usuarios", json=user_data) # Tenta criar
            response = requests.post(LOGIN_URL, json=user_data)
            if response.status_code == 200:
                 return response.json().get("token")
            
        print(f"❌ Falha no login: {response.text}")
        return None
    except Exception as e:
        print(f"❌ Erro de conexão no login: {e}")
        return None

def run_test():
    print("🚀 Teste de processamento OTIMIZADO (Threading Paralelo + Bulk Insert)")
    print("=" * 80)
    print(f"📡 API URL: {BASE_URL}")
    print(f"📂 Arquivo Input: {INPUT_FILE}")

    # Autenticação
    token = get_token()
    if not token:
        print("❌ Não foi possível autenticar. Abortando teste.")
        sys.exit(1)

    print()

    # Abrir arquivo
    print(f"📂 Lendo arquivo...")
    with open(INPUT_FILE, 'rb') as f:
        files = {'file': (INPUT_FILE, f, 'text/csv')}
        headers = {'Authorization': f'Bearer {token}'}
        
        print(f"📤 Enviando para: {BATCH_URL}")
        print("⏳ Aguardando processamento...")
        
        inicio = time.time()
        
        try:
            response = requests.post(
                BATCH_URL, 
                files=files,
                headers=headers,
                timeout=120
            )
            
            duracao = time.time() - inicio
            
            print("=" * 80)
            print(f"✅ Resposta recebida em {duracao:.2f} segundos")
            print(f"📊 Status Code: {response.status_code}")
            
            if response.status_code == 200:
                output_file = "resultado_optimized_oci.csv"
                with open(output_file, 'wb') as out:
                    out.write(response.content)
                
                print(f"✅ Arquivo salvo: {output_file}")
                
                # Análise simples
                lines = response.text.splitlines()
                total = len(lines) - 1 if len(lines) > 0 else 0
                print(f"📋 Total processado: {total} registros")
                
                if duracao > 0:
                    speed = total / duracao
                    print(f"⚡ Velocidade: {speed:.2f} rec/s")
                
                print("\n🎉 TESTE DE BATCH SUCESSO!")
            else:
                print(f"❌ Erro no processamento: {response.text[:200]}")
                sys.exit(1)
                
        except Exception as e:
            print(f"❌ Erro na requisição: {e}")
            sys.exit(1)

if __name__ == "__main__":
    run_test()
