import time
import os
import subprocess
import sys

# Intervalo de verificação em segundos
CHECK_INTERVAL = 3
# FIXED: Point to the correct script location in scripts/ folder
SCRIPT_TO_RUN = os.path.join("scripts", "leitor_contexto_pdr.py") 
WATCH_DIR = "."

def get_last_modified_time(directory):
    """Retorna o timestamp da modificação mais recente em toda a árvore de diretórios."""
    latest_mtime = 0
    ignore_dirs = {".git", ".terraform", ".vscode", ".idea", "__pycache__", "node_modules", "venv", ".oci", "target"}
    
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        
        for file in files:
            if file == "PROJECT_CONTEXT_SUMMARY.txt": continue
            
            try:
                path = os.path.join(root, file)
                mtime = os.path.getmtime(path)
                if mtime > latest_mtime:
                    latest_mtime = mtime
            except OSError:
                continue
    return latest_mtime

def main():
    print(f"👀 Monitorando alterações em '{os.path.abspath(WATCH_DIR)}'...")
    print(f"🔄 O arquivo de contexto será atualizado automaticamente.")
    print("Pressione Ctrl+C para parar.")
    
    last_processed_mtime = get_last_modified_time(WATCH_DIR)
    
    # Executa uma vez no início
    if os.path.exists(SCRIPT_TO_RUN):
        subprocess.run([sys.executable, SCRIPT_TO_RUN])
    else:
        print(f"❌ Erro: Script {SCRIPT_TO_RUN} não encontrado.")

    try:
        while True:
            time.sleep(CHECK_INTERVAL)
            current_mtime = get_last_modified_time(WATCH_DIR)
            
            if current_mtime > last_processed_mtime:
                print(f"\n[Detectada alteração] Atualizando contexto...")
                if os.path.exists(SCRIPT_TO_RUN):
                    subprocess.run([sys.executable, SCRIPT_TO_RUN])
                else:
                    print(f"❌ Erro: Script {SCRIPT_TO_RUN} não encontrado.")
                last_processed_mtime = current_mtime
                print("✅ Contexto atualizado.")
                
    except KeyboardInterrupt:
        print("\nMonitoramento encerrado.")

if __name__ == "__main__":
    main()
