
import csv
import random
import requests
import time
import os

# Configuração
ARQUIVO_1K = "teste_1k.csv"
URL_BATCH = "http://localhost:9999/api/churn/batch/optimized"
LOGIN_URL = "http://localhost:9999/login"
TIMEOUT_SECONDS = 600

def gerar_csv_1k():
    print("🔨 Gerando CSV com 1.000 registros...")
    header = ["cliente_id", "idade", "genero", "tempo_assinatura_meses", "plano_assinatura", "valor_mensal", "visualizacoes_mes", "tempo_medio_sessao_min", "contatos_suporte", "avaliacao_conteudo_media", "avaliacao_conteudo_ultimo_mes", "avaliacao_plataforma", "regiao"]
    
    with open(ARQUIVO_1K, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        
        planos = ["Basico", "Premium", "Familia"]
        regioes = ["Norte", "Sul", "Leste", "Oeste", "Sudeste"]
        
        for i in range(1000):
            writer.writerow([
                f"CLI-{i:04d}",
                random.randint(18, 80),
                random.choice(["Masculino", "Feminino"]),
                random.randint(1, 60),
                random.choice(planos),
                round(random.uniform(20.0, 100.0), 2),
                random.randint(0, 50),
                random.randint(5, 120),
                random.randint(0, 10),
                round(random.uniform(1.0, 5.0), 1),
                round(random.uniform(1.0, 5.0), 1),
                round(random.uniform(1.0, 5.0), 1),
                random.choice(regioes)
            ])
    print(f"✅ CSV gerado: {ARQUIVO_1K}")

def get_token():
    print("🔑 Autenticando...")
    reg_url = "http://localhost:9999/usuarios"
    user = {"login": "user_1k", "senha": "123"}
    try:
        requests.post(reg_url, json=user)
    except: pass
    
    try:
        response = requests.post(LOGIN_URL, json=user)
        if response.status_code == 200:
            return response.json().get("token")
        else:
            print(f"❌ Falha auth: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Erro auth: {e}")
        return None

def run_test():
    if not os.path.exists(ARQUIVO_1K):
        gerar_csv_1k()
        
    token = get_token()
    if not token: return

    files = {'file': (ARQUIVO_1K, open(ARQUIVO_1K, 'rb'), 'text/csv')}
    headers = {'Authorization': f'Bearer {token}'}
    
    print(f"📤 Enviando 1.000 linhas...")
    inicio = time.time()
    try:
        response = requests.post(URL_BATCH, files=files, headers=headers, timeout=TIMEOUT_SECONDS)
        duracao = time.time() - inicio
        
        if response.status_code == 200:
            print(f"✅ SUCESSO! Tempo: {duracao:.2f}s")
        else:
            print(f"❌ ERRO: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Falha: {e}")

if __name__ == "__main__":
    run_test()
