import requests
import time

def get_token():
    """Autentica e retorna o token JWT"""
    print("🔑 Autenticando...")
    login_url = "http://localhost:9999/login"
    register_url = "http://localhost:9999/usuarios"
    user_data = {"login": "test_batch_user", "senha": "123"}
    
    # Tentar cadastrar (pode falhar se já existir)
    try:
        requests.post(register_url, json=user_data)
    except:
        pass
    
    # Fazer login
    response = requests.post(login_url, json=user_data)
    if response.status_code == 200:
        token = response.json().get("token")
        print("✅ Login realizado com sucesso!")
        return token
    else:
        print("❌ Falha no login")
        return None

print("🚀 Teste de processamento OTIMIZADO (Threading Paralelo + Bulk Insert)")
print("=" * 80)

# Autenticação
token = get_token()
if not token:
    print("❌ Não foi possível autenticar. Abortando teste.")
    exit(1)

print()

# Configuração
url_optimized = "http://localhost:9999/api/churn/batch/optimized"
arquivo = "teste_batch.csv"  # Começar com arquivo pequeno para validar

# Abrir arquivo
print(f"📂 Abrindo arquivo: {arquivo}")
with open(arquivo, 'rb') as f:
    files = {'file': (arquivo, f, 'text/csv')}
    headers = {'Authorization': f'Bearer {token}'}
    
    print(f"📤 Enviando para: {url_optimized}")
    print("⚙️  Configuração do servidor: 20 threads paralelas + bulk insert 1000")
    print("⏳ Aguardando processamento...")
    print()
    
    inicio = time.time()
    
    try:
        response = requests.post(
            url_optimized, 
            files=files,
            headers=headers,
            timeout=120  # 2 minutos
        )
        
        fim = time.time()
        duracao = fim - inicio
        
        print("=" * 80)
        print(f"✅ Resposta recebida!")
        print(f"⏱️  Tempo total: {duracao:.2f} segundos")
        print(f"📊 Status Code: {response.status_code}")
        print(f"📦 Tamanho da resposta: {len(response.content)} bytes")
        print()
        
        if response.status_code == 200:
            # Salvar resultado
            output_file = "resultado_optimized.csv"
            with open(output_file, 'wb') as out:
                out.write(response.content)
            
            print(f"✅ Arquivo salvo: {output_file}")
            
            # Contar linhas
            with open(output_file, 'r', encoding='utf-8') as f:
                linhas = len(f.readlines())
            
            clientes_processados = linhas - 1
            print(f"📋 Total processado: {clientes_processados} clientes")
            print()
            
            # Mostrar primeiras linhas do resultado
            print("📄 Primeiras 3 linhas do resultado:")
            print("-" * 80)
            with open(output_file, 'r', encoding='utf-8') as f:
                for i, linha in enumerate(f):
                    if i < 4:  # header + 3 linhas
                        # Truncar linha muito longa
                        linha_display = linha.strip()
                        if len(linha_display) > 120:
                            linha_display = linha_display[:120] + "..."
                        print(linha_display)
            print("-" * 80)
            print()
            
            # Calcular velocidade
            if duracao > 0:
                clientes_por_segundo = clientes_processados / duracao
                print(f"⚡ VELOCIDADE: {clientes_por_segundo:.2f} clientes/segundo")
                
                # Projeção para 50k
                tempo_50k_segundos = 50000 / clientes_por_segundo
                tempo_50k_minutos = tempo_50k_segundos / 60
                print(f"📈 Projeção para 50.000 clientes: {tempo_50k_minutos:.1f} minutos")
            
            print()
            print("🎉 TESTE CONCLUÍDO COM SUCESSO!")
            print()
            print("✨ OTIMIZAÇÕES APLICADAS:")
            print("  ✅ Threading paralelo (20 workers simultâneos)")
            print("  ✅ Bulk insert MongoDB (1000 registros por vez)")
            print("  ✅ CompletableFuture para processamento assíncrono")
            
        else:
            print(f"❌ Erro no processamento!")
            print(f"Response: {response.text[:500]}")
            
    except requests.exceptions.Timeout:
        print("⏰ TIMEOUT! O processamento excedeu 2 minutos.")
    except Exception as e:
        print(f"❌ Erro: {e}")

print("=" * 80)
