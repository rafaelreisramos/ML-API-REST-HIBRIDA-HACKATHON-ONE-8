import requests
import time

print("🚀 Iniciando teste de processamento em lote (50.000 clientes)...")
print("=" * 70)

# Configuração
url = "http://localhost:9999/api/churn/batch"
arquivo = "simulacao_futura_50000_clientes (1).csv"

# Abrir arquivo
print(f"📂 Abrindo arquivo: {arquivo}")
with open(arquivo, 'rb') as f:
    files = {'file': (arquivo, f, 'text/csv')}
    
    print(f"📤 Enviando para: {url}")
    print("⏳ Aguardando processamento (pode levar vários minutos)...")
    print()
    
    inicio = time.time()
    
    try:
        response = requests.post(
            url, 
            files=files,
            timeout=600  # 10 minutos
        )
        
        fim = time.time()
        duracao = fim - inicio
        
        print("=" * 70)
        print(f"✅ Resposta recebida!")
        print(f"⏱️  Tempo total: {duracao:.2f} segundos ({duracao/60:.2f} minutos)")
        print(f"📊 Status Code: {response.status_code}")
        print(f"📦 Tamanho da resposta: {len(response.content)} bytes")
        print()
        
        if response.status_code == 200:
            # Salvar resultado
            output_file = "resultado_50000.csv"
            with open(output_file, 'wb') as out:
                out.write(response.content)
            
            print(f"✅ Arquivo salvo: {output_file}")
            
            # Contar linhas
            with open(output_file, 'r', encoding='utf-8') as f:
                linhas = len(f.readlines())
            
            print(f"📋 Total de linhas processadas: {linhas - 1} (+ header)")
            print()
            
            # Mostrar primeiras linhas do resultado
            print("📄 Primeiras 3 linhas do resultado:")
            print("-" * 70)
            with open(output_file, 'r', encoding='utf-8') as f:
                for i, linha in enumerate(f):
                    if i < 4:  # header + 3 linhas
                        print(linha.strip())
            print("-" * 70)
            
            # Calcular velocidade
            clientes_por_segundo = (linhas - 1) / duracao
            print(f"⚡ Velocidade: {clientes_por_segundo:.2f} clientes/segundo")
            print()
            print("🎉 TESTE CONCLUÍDO COM SUCESSO!")
            
        else:
            print(f"❌ Erro no processamento!")
            print(f"Response: {response.text[:500]}")
            
    except requests.exceptions.Timeout:
        print("⏰ TIMEOUT! O processamento excedeu 10 minutos.")
        print("💡 Considere processar em lotes menores ou aumentar o timeout.")
    except Exception as e:
        print(f"❌ Erro: {e}")

print("=" * 70)
