# -*- coding: utf-8 -*-
import os
import sys
import time
import requests
import random
import subprocess
from datetime import datetime

# --- CONFIGURAÇÃO MANUAL PARA LOCALHOST ---
BASE_URL = os.getenv("API_URL", "http://localhost:9999")
LOGIN_URL = f"{BASE_URL}/login"
BATCH_URL = f"{BASE_URL}/api/churn/batch/optimized"

# Cores
C_RESET  = "\033[0m"
C_RED    = "\033[91m"
C_GREEN  = "\033[92m"
C_YELLOW = "\033[93m"
C_BLUE   = "\033[94m"
C_MAGENTA= "\033[95m"
C_CYAN   = "\033[96m"
C_BOLD   = "\033[1m"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    clear_screen()
    print(f"{C_BLUE}" + "="*80)
    print(f"{C_BOLD}   CHURN INSIGHT - ORQUESTRADOR DE DEMONSTRAÇÃO (LOCAL){C_RESET}")
    print(f"   {C_CYAN}Ambiente: LOCALHOST (Dev/Test){C_RESET}")
    print(f"   {C_CYAN}API URL : {BASE_URL}{C_RESET}")
    print(f"{C_BLUE}" + "="*80 + f"{C_RESET}\n")

def get_token():
    print(f"🔑 {C_YELLOW}Autenticando admin...{C_RESET}")
    try:
        resp = requests.post(LOGIN_URL, json={"login": "admin", "senha": "123456"}, timeout=5)
        if resp.status_code == 200:
            print(f"✅ {C_GREEN}Token recebido!{C_RESET}\n")
            return resp.json().get("token")
        else:
            print(f"❌ {C_RED}Login falhou: {resp.status_code}{C_RESET}")
            return None
    except Exception as e:
        print(f"❌ {C_RED}Erro de conexão: {e}{C_RESET}")
        return None

# --- GERADOR DE DADOS ---
def generate_chunk(start_id, count):
    """Gera um bloco de CSV na memória para envio imediato"""
    csv_lines = []
    header = "clienteId,idade,genero,regiao,valorMensal,tempoAssinaturaMeses,diasUltimoAcesso,avaliacaoPlataforma,avaliacaoConteudoMedia,avaliacaoConteudoUltimoMes,tempoMedioSessaoMin,planoAssinatura,metodoPagamento,dispositivoPrincipal,visualizacoesMes,contatosSuporte,tipoContrato,categoriaFavorita,acessibilidade"
    csv_lines.append(header)
    
    for i in range(count):
        cid = start_id + i
        risk = random.random() > 0.6
        idade = random.randint(18, 80)
        dias = random.randint(15, 60) if risk else random.randint(0, 10)
        aval = random.uniform(1.0, 3.5) if risk else random.uniform(4.0, 5.0)
        
        line = f"LOAD-{cid:05d},{idade},Simulado,Nuvem,59.90,12,{dias},{aval:.1f},4.0,4.0,45,Premium,Pix,Mobile,10,0,MENSAL,ACAO,0"
        csv_lines.append(line)
    
    return "\n".join(csv_lines)

# --- MODO 3: STRESS TEST ---
def run_stress_test():
    token = get_token()
    if not token: return

    TARGET_TOTAL = 50000 
    CHUNK_SIZE = 2000    
    
    print(f"{C_MAGENTA}🔥 INICIANDO TESTE DE CARGA MASSIVA (STRESS TEST){C_RESET}")
    print(f"   Meta: {C_BOLD}{TARGET_TOTAL:,}{C_RESET} registros")
    print(f"   Estratégia: Streaming por Micro-Lotes ({CHUNK_SIZE} req/lote)")
    print("-" * 80)
    print("Prepare-se para os logs... (Pressione Ctrl+C para parar prematuramente)")
    time.sleep(2)
    
    total_processed = 0
    total_churn = 0
    start_time = time.time()
    
    try:
        while total_processed < TARGET_TOTAL:
            current_chunk_size = min(CHUNK_SIZE, TARGET_TOTAL - total_processed)
            csv_data = generate_chunk(total_processed, current_chunk_size)
            
            tmp_file = "temp_stress_chunk.csv"
            with open(tmp_file, "w", encoding="utf-8") as f:
                f.write(csv_data)
            
            batch_start = time.time()
            
            sys.stdout.write(f"\r{C_YELLOW}⚡ Enviando lote {total_processed}-{total_processed+current_chunk_size}...{C_RESET}")
            
            with open(tmp_file, 'rb') as f:
                files = {'file': (tmp_file, f, 'text/csv')}
                headers = {'Authorization': f'Bearer {token}'}
                try:
                    resp = requests.post(BATCH_URL, files=files, headers=headers, timeout=120)
                except requests.exceptions.Timeout:
                    print(f"\n{C_RED}❌ Timeout no lote! Reduzindo tamanho...{C_RESET}")
                    continue
            
            batch_time = time.time() - batch_start
            
            if resp.status_code == 200:
                lines = resp.text.splitlines()
                data_lines = [l for l in lines if "clienteId" not in l and "," in l]
                
                churn_in_batch = 0
                sample_size = min(10, len(data_lines)) 
                
                print(f"\r✅ Lote processado em {batch_time:.2f}s | Speed: {current_chunk_size/batch_time:.0f} rec/s")
                
                for line in data_lines:
                    if "ALTO" in str(line).upper() or "0.428" in line or "0.5" in line:
                         churn_in_batch += 1

                for i in range(sample_size):
                    l = data_lines[i]
                    parts = l.split(',')
                    pid = parts[0]
                    risk = "ALTO" in str(l).upper()
                    
                    color = C_RED if risk else C_GREEN
                    status = "ALERTA" if risk else "OK"
                    print(f"   [{datetime.now().strftime('%H:%M:%S')}] PROC: {pid} -> {color}{status}{C_RESET}")
                
                print(f"   {C_CYAN}... e mais {len(data_lines)-sample_size} registros processados em background.{C_RESET}")
                
                total_processed += len(data_lines)
                total_churn += churn_in_batch
                
                progress = (total_processed / TARGET_TOTAL) * 100
                elapsed_total = time.time() - start_time
                avg_speed = total_processed / elapsed_total if elapsed_total > 0 else 0
                
                print(f"{C_BLUE}[PROGRESSO] {progress:.1f}% completo | Total: {total_processed:,} | Churn Identificado: {total_churn:,} | Vel: {avg_speed:.0f} rec/s{C_RESET}")
                print("-" * 40)
                
            else:
                print(f"\n{C_RED}❌ Erro no lote: {resp.status_code} - {resp.text[:100]}{C_RESET}")
                time.sleep(2)

    except KeyboardInterrupt:
        print(f"\n\n{C_YELLOW}⚠ Teste interrompido pelo usuário.{C_RESET}")
    
    end_time = time.time()
    total_time = end_time - start_time
    
    print("\n" + "="*80)
    print(f"{C_BOLD}🏁 RELATÓRIO DE TESTE DE CARGA{C_RESET}")
    print("="*80)
    print(f"⏱️  Tempo Total       : {total_time/60:.2f} minutos")
    print(f"📦 Total Processado  : {C_BOLD}{total_processed:,}{C_RESET} registros")
    print(f"🚨 Total Churn (IA)  : {C_RED}{total_churn:,}{C_RESET} clientes identificados")
    print(f"⚡ Velocidade Média  : {C_BOLD}{total_processed/total_time:.0f}{C_RESET} registros/segundo")
    
    if total_time > 0:
        proj_hour = (total_processed/total_time) * 3600
        print(f"📈 Projeção/Hora     : {proj_hour:,.0f} requisições")
    
    input(f"\n{C_BOLD}Pressione Enter para voltar ao menu...{C_RESET}")


# --- MENU PRINCIPAL ---
def main():
    while True:
        print_banner()
        print("Selecione o modo de demonstração:")
        print(f"1. {C_GREEN}🧪 Validação Técnica Rápida{C_RESET} (Scripts de Teste)")
        print(f"2. {C_CYAN}📊 Demo Visual Executiva{C_RESET} (100 Clientes Reais)")
        print(f"3. {C_MAGENTA}🔥 Teste de Carga Extremo{C_RESET} (50k Registros - 8 min limit)")
        print("0. Sair")
        
        opt = input("\n> ")
        
        if opt == "1":
            # MODIFICACAO: CHAMA O MODO LOCAL
            subprocess.call([r"run_tests_local.bat"], cwd=r"developer_tools\scripts", shell=True)
            input("\nEnter para continuar...")
        
        elif opt == "2":
            subprocess.call(["python", r"developer_tools\scripts\demo_dashboard.py"])
            input("\nEnter para continuar...")
            
        elif opt == "3":
            run_stress_test()
            
        elif opt == "0":
            print("Até logo!")
            sys.exit(0)
        else:
            print("Opção inválida!")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
