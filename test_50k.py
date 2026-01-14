import requests
import time

# Configuração
ARQUIVO_50K = "teste_50k_correto.csv"
URL_BATCH = "http://localhost:9999/api/churn/batch/optimized"
LOGIN_URL = "http://localhost:9999/login"
TIMEOUT_SECONDS = 600  # 10 minutos (50k leva tempo!)

def get_token():
    """Autentica e retorna o token JWT"""
    print("🔑 Autenticando...")
    try:
        # Tentar registrar usuário de teste primeiro
        reg_url = "http://localhost:9999/usuarios"
        user = {"login": "user_50k", "senha": "123"}
        try:
            requests.post(reg_url, json=user)
        except:
            pass # Ignorar se já existe

        response = requests.post(LOGIN_URL, json=user)
        if response.status_code == 200:
            print("✅ Login realizado com sucesso!")
            return response.json().get("token")
        else:
            print(f"❌ Falha no login: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Erro de conexão no login: {e}")
        return None

def run_large_test():
    print(f"🚀 Iniciando teste de carga com arquivo: {ARQUIVO_50K}")
    
    token = get_token()
    if not token:
        return

    print(f"📂 Lendo arquivo de {ARQUIVO_50K}...")
    try:
        f = open(ARQUIVO_50K, 'rb')
    except FileNotFoundError:
        print("❌ Arquivo não encontrado! Gere-o primeiro com 'python scripts/generate_large_csv.py'")
        return

    files = {'file': (ARQUIVO_50K, f, 'text/csv')}
    headers = {'Authorization': f'Bearer {token}'}

    print(f"📤 Enviando 50.000 linhas para: {URL_BATCH}")
    print("⏳ Aguardando processamento (isso pode levar alguns minutos)...")
    
    inicio = time.time()
    
    try:
        response = requests.post(
            URL_BATCH, 
            files=files,
            headers=headers,
            timeout=TIMEOUT_SECONDS
        )
        
        fim = time.time()
        duracao = fim - inicio
        
        print("\n" + "=" * 60)
        if response.status_code == 200:
            print(f"✅ SUCESSO! Processamento concluído.")
            print(f"⏱️  Tempo total: {duracao:.2f} segundos")
            print(f"📦 Tamanho da resposta: {len(response.content) / 1024:.2f} KB")
            
            # Salvar retorno
            output = "resultado_50k.csv"
            with open(output, 'wb') as out:
                out.write(response.content)
            print(f"💾 Resultado salvo em: {output}")
        else:
            print(f"❌ ERRO HTTP {response.status_code}")
            print(f"Detalhe: {response.text[:500]}")
            
    except requests.exceptions.Timeout:
        print(f"⏰ TIMEOUT! O backend demorou mais que {TIMEOUT_SECONDS}s.")
    except Exception as e:
        print(f"❌ Erro de requisição: {e}")
    finally:
        f.close()

if __name__ == "__main__":
    run_large_test()
