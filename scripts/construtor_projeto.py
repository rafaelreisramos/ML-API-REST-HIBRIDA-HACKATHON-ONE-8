import os
import re
import sys
import codecs

def reconstruct_project(context_file="PROJECT_CONTEXT_PDR.txt", output_dir="."):
    """
    Lê um arquivo de contexto (PDR ou SUMMARY) e recria a estrutura de arquivos e pastas original.
    """
    if not os.path.exists(context_file):
        print(f"❌ Arquivo de contexto '{context_file}' não encontrado.")
        print(f"   Certifique-se de que o arquivo está no diretório atual ou passe o caminho como argumento.")
        return

    print(f"🔨 Iniciando reconstrução (Hidratação) a partir de: {context_file}")
    
    # Tentativa de leitura robusta (UTF-8 -> Latin-1)
    content = ""
    try:
        with open(context_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        print("⚠️  Aviso: Falha ao ler como UTF-8. Tentando fallback para LATIN-1...")
        try:
            with open(context_file, 'r', encoding='latin-1') as f:
                content = f.read()
        except Exception as e:
            print(f"❌ ERRO FATAL: Não foi possível ler o arquivo de contexto: {e}")
            return
    except Exception as e:
        print(f"❌ ERRO FATAL ao abrir arquivo: {e}")
        return

    # Regex robusto para capturar cabeçalhos.
    pattern = re.compile(
        r'(?:^|\n)={80}\n(?:📄 )?ARQUIVO: (.+?)\n-{80}(?:\n|$)',
        re.MULTILINE
    )

    matches = list(pattern.finditer(content))

    if not matches:
        print("⚠️  Nenhum marcador de arquivo encontrado.")
        print("   Verifique se o arquivo segue o formato padrão de contexto (Separadores de 80 '=').")
        return

    print(f"📦 Encontrados {len(matches)} arquivos para restaurar...")

    restored_count = 0
    skipped_count = 0
    errors = []

    for i, match in enumerate(matches):
        file_path_raw = match.group(1).strip()
        file_path = os.path.normpath(file_path_raw)

        # O conteúdo começa exatamente onde o match (cabeçalho) termina
        start_index = match.end()
        
        if i + 1 < len(matches):
            end_index = matches[i+1].start()
        else:
            end_index = len(content)

        # O conteúdo bruto extraído
        file_content = content[start_index:end_index]

        # Limpeza Cirúrgica (Trim Smart)
        if file_content.startswith("\n"):
            file_content = file_content[1:]
        if file_content.endswith("\n"):
            file_content = file_content[:-1]
            
        # Caminho completo de saída
        full_path = os.path.join(output_dir, file_path)
        
        # Segurança: Não sobrescrever o próprio arquivo de contexto
        if os.path.abspath(full_path) == os.path.abspath(context_file):
            print(f"  ⏭️  Ignorando o próprio arquivo fonte: {file_path}")
            skipped_count += 1
            continue

        # Segurança: Evitar caminhos suspeitos
        if ".." in file_path:
             print(f"  ⚠️  Caminho suspeito ignorado: {file_path}")
             skipped_count += 1
             errors.append(f"{file_path} (Path Traversal Detection)")
             continue

        # Criar diretórios necessários
        dir_name = os.path.dirname(full_path)
        try:
            if dir_name:
                os.makedirs(dir_name, exist_ok=True)
        except OSError as e:
             print(f"  ❌ Erro ao criar diretório {dir_name}: {e}")
             skipped_count += 1
             errors.append(f"{file_path} (Directory Creation Failed)")
             continue
            
        # Escrever arquivo
        try:
            with open(full_path, 'w', encoding='utf-8') as outfile:
                outfile.write(file_content)
            # print(f"  ✅ Restaurado: {file_path}") # Comentado para reduzir ruído em listas grandes
            restored_count += 1
            # Imprimir um pontinho a cada 10 arquivos para mostrar progresso sem spam
            if restored_count % 10 == 0:
                print(".", end="", flush=True)

        except PermissionError:
            print(f"\n  ❌ Erro de PERMISSÃO ao escrever {file_path}. Arquivo em uso ou protegido.")
            skipped_count += 1
            errors.append(f"{file_path} (Permission Denied)")
        except Exception as e:
            print(f"\n  ❌ Erro desconhecido ao escrever {file_path}: {e}")
            skipped_count += 1
            errors.append(f"{file_path} ({str(e)})")

    print(f"\n\n✨ Reconstrução concluída!")
    print(f"   ✅ Arquivos restaurados: {restored_count}")
    print(f"   ⚠️  Arquivos ignorados/erros: {skipped_count}")
    
    if errors:
        print("\n📋 Relatório de Erros:")
        for err in errors:
            print(f"   - {err}")

if __name__ == "__main__":
    target_file = sys.argv[1] if len(sys.argv) > 1 else "PROJECT_CONTEXT_PDR.txt"
    reconstruct_project(target_file)
