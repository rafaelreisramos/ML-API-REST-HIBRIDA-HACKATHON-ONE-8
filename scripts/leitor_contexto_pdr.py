import os

# Configurações
ROOT_DIR = "."
OUTPUT_FILE = "PROJECT_CONTEXT_PDR.txt"

# Ignorar pastas de sistema/build/libs
IGNORE_DIRS = {
    ".git", ".terraform", ".vscode", ".idea", "__pycache__", 
    "node_modules", "venv", ".venv_wsl", ".oci", "dist", "build", "coverage"
}

# Ignorar extensões binárias ou desnecessárias
IGNORE_EXTENSIONS = {
    ".exe", ".dll", ".so", ".bin", ".box", ".zip", ".tar", ".gz", 
    ".png", ".jpg", ".jpeg", ".gif", ".ico", ".pdf", ".tfstate", 
    ".tfstate.backup", ".pyc", ".class", ".joblib", ".pkl", ".db", ".sqlite3"
}

# Ignorar arquivos específicos grandes ou de lock
IGNORE_FILES = {
    "package-lock.json", "yarn.lock", "pnpm-lock.yaml", 
    "dataset_churn_streaming_3000_registros.csv", 
    "resultado_previsoes_batch.csv",
    "PROJECT_CONTEXT_SUMMARY.txt", # Ignora o outro contexto
    OUTPUT_FILE
}

def is_text_file(filename):
    """Verifica se não é uma extensão ignorada (binária ou dados pesados)."""
    return not any(filename.endswith(ext) for ext in IGNORE_EXTENSIONS | {".csv"})

def get_file_priority(filename):
    """
    Define a 'ordem de apresentação' do PDR.
    1. Documentação (.md) -> Lê primeiro quem explica o projeto.
    2. Configuração (requirements, docker) -> Entende o ambiente.
    3. Código Core (.py) -> Entende a lógica do backend.
    4. Código Frontend (.tsx, .ts) -> Entende a tela.
    5. Resto.
    """
    if filename.endswith(".md"): return 0        # Docs
    if "docker" in filename.lower() or "requirements" in filename.lower(): return 1 # Configs
    if filename.endswith(".py"): return 2        # Backend
    if filename.endswith("json"): return 3       # Configs JS
    if filename.endswith(".tsx") or filename.endswith(".ts"): return 4 # Frontend
    return 5

def generate_pdr_context():
    print(f"🔍 Gerando Contexto PDR em: {os.path.abspath(ROOT_DIR)}...")
    
    all_files_to_read = []
    
    # 1. Caminhada (Walk) para coletar arquivos válidos
    for root, dirs, files in os.walk(ROOT_DIR):
        # Filtrar pastas ignoradas (Modifica dirs in-place)
        # Reforçando bloqueio de venv/node_modules
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS and not d.startswith('.venv')]
        
        # Bloqueio extra de segurança para caminhos completos
        if ".venv" in root or "node_modules" in root or "__pycache__" in root:
            continue
        
        for file in files:
            file_path = os.path.join(root, file)
            
            # Filtros de exclusão
            if file in IGNORE_FILES: continue
            if not is_text_file(file): continue
            
            all_files_to_read.append(file_path)

    # 2. Ordenação Inteligente (Prioridade PDR + Ordem Alfabética)
    # A tupla de ordenação funciona assim: Primeiro pelo "Grupo" (0 a 5), desempate pelo Caminho.
    all_files_to_read.sort(key=lambda p: (get_file_priority(os.path.basename(p)), p))

    # 3. Escrita do Arquivo
    with open(OUTPUT_FILE, "w", encoding="utf-8") as outfile:
        # Cabeçalho do "PDR"
        outfile.write(f"# PROJECT CONTEXT & PDR: {os.path.basename(os.path.abspath(ROOT_DIR))}\n")
        outfile.write(f"# Documento Gerado Automaticamente para Contextualização de IA\n")
        outfile.write(f"# Estrutura: Documentação -> Configuração -> Backend -> Frontend\n")
        outfile.write("="*80 + "\n\n")

        total_files = 0
        
        for file_path in all_files_to_read:
            relative_path = os.path.relpath(file_path, ROOT_DIR)
            
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as infile:
                    content = infile.read()
                    
                    # Evitar arquivos vazios ou muito pequenos irrelevantes
                    if not content.strip(): continue

                    # Formatação visual clara para a IA separar os arquivos
                    outfile.write(f"\n{'='*80}\n")
                    outfile.write(f"📄 ARQUIVO: {relative_path}\n")
                    outfile.write(f"{'-'*80}\n")
                    outfile.write(content + "\n")
                    
                    print(f"  ✅ Lido: {relative_path}")
                    total_files += 1
                    
            except Exception as e:
                print(f"  ❌ Erro ao ler {relative_path}: {e}")

    print(f"\n✨ Sucesso! {total_files} arquivos compilados em: {OUTPUT_FILE}")
    print(f"Este arquivo está ordenado para contar a 'história' do projeto (Docs -> Code).")

if __name__ == "__main__":
    generate_pdr_context()
