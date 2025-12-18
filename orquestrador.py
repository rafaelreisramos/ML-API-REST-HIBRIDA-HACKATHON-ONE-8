import os
import sys
import subprocess
import time

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    print("=" * 60)
    print("       🚀 SISTEMA DE TELETRANSPORTE DE PROJETOS 🌌")
    print("             Ferramentas de Contexto & IA")
    print("=" * 60)

def menu():
    while True:
        clear_screen()
        print_header()
        print("\nEscolha uma operação:")
        print(" [1] 📸 GERAR Contexto (Backup/PDR) -> Cria arquivo único do projeto")
        print(" [2] 🏗️  RESTAURAR Projeto (Teleporte) -> Recria arquivos a partir do contexto")
        print(" [3] 🤖 Iniciar Monitor Automático (Daemon) -> Mantém contexto atualizado")
        print(" [0] Sair")
        
        choice = input("\nOpção: ").strip()
        
        if choice == '1':
            run_generator()
        elif choice == '2':
            run_restore()
        elif choice == '3':
            run_daemon()
        elif choice == '0':
            print("Até logo! 👋")
            sys.exit()
        else:
            print("Opção inválida!")
            time.sleep(1)

def run_generator():
    clear_screen()
    print_header()
    print("📸 Iniciando Gerador de Contexto...")
    script_path = os.path.join("scripts", "leitor_contexto_pdr.py")
    
    if not os.path.exists(script_path):
        print(f"❌ Erro: Script {script_path} não encontrado.")
        input("Pressione Enter para voltar...")
        return

    subprocess.run([sys.executable, script_path])
    input("\n✅ Processo finalizado. Pressione Enter para voltar...")

def run_restore():
    clear_screen()
    print_header()
    print("🏗️  Modo de Restauração")
    print("Certifique-se que o arquivo de contexto (PDR ou SUMMARY) está nesta pasta.")
    
    context_file = input("Nome do arquivo de contexto [Enter para 'PROJECT_CONTEXT_PDR.txt']: ").strip()
    if not context_file:
        context_file = "PROJECT_CONTEXT_PDR.txt"
        
    script_path = os.path.join("scripts", "construtor_projeto.py")
    
    if not os.path.exists(script_path):
        print(f"❌ Erro: Script {script_path} não encontrado.")
        input("Pressione Enter para voltar...")
        return

    subprocess.run([sys.executable, script_path, context_file])
    input("\n✅ Processo finalizado. Pressione Enter para voltar...")

def run_daemon():
    clear_screen()
    print("🤖 Iniciando Monitor de Contexto...")
    # Assume que auto_leitor está na raiz
    if os.path.exists("auto_leitor.py"):
        subprocess.run([sys.executable, "auto_leitor.py"])
    else:
        print("❌ auto_leitor.py não encontrado na raiz.")
        input()

if __name__ == "__main__":
    menu()
