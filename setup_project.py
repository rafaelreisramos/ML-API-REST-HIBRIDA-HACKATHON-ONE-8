#!/usr/bin/env python3
"""
Script de Setup do Projeto - Zero Config
Copia artefatos necessários do time de Data Science para o AI Service
"""
import os
import shutil
from pathlib import Path

def main():
    print("🚀 Iniciando Setup do Projeto...")
    
    # Diretórios
    source_dir = Path("hackathon_g8_one")
    ai_models_dir = Path("ai_service/models")
    
    # Criar pasta de modelos se não existir
    ai_models_dir.mkdir(parents=True, exist_ok=True)
    
    # Arquivos para copiar
    files_to_copy = [
        ("data/X_train.csv", "X_train.csv"),
        ("data/y_train.csv", "y_train.csv"),
        ("models/rfe_selector.joblib", "rfe_selector.joblib"),
        ("models/threshold_otimo.txt", "threshold_otimo.txt"),
    ]
    
    copied = 0
    for source_file, dest_file in files_to_copy:
        source_path = source_dir / source_file
        dest_path = ai_models_dir / dest_file
        
        if source_path.exists():
            shutil.copy2(source_path, dest_path)
            print(f"✅ Copiado: {source_file} -> {dest_path}")
            copied += 1
        else:
            print(f"⚠️  Não encontrado: {source_path}")
    
    print(f"\n✨ Setup concluído! {copied}/{len(files_to_copy)} arquivos copiados.")
    print("💡 O AI Service agora pode usar Auto-Healing para reconstruir o modelo.")

if __name__ == "__main__":
    main()
