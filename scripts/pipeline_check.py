import os
import sys

def check_environment():
    print("🔍 Diagnosticando Pipeline de Teletransporte...")
    
    status = {"OK": [], "MISSING": []}
    
    required_files = [
        "scripts/leitor_contexto_pdr.py",
        "scripts/construtor_projeto.py",
        "orquestrador.py",
        "auto_leitor.py"
    ]
    
    for f in required_files:
        if os.path.exists(f):
            status["OK"].append(f)
            print(f"  ✅ [OK] {f}")
        else:
            status["MISSING"].append(f)
            print(f"  ❌ [FALTA] {f}")
            
    print("-" * 40)
    if status["MISSING"]:
        print(f"⚠️  Atenção: {len(status['MISSING'])} componentes críticos estão faltando.")
        print("    O sistema pode não funcionar corretamente.")
        return False
    else:
        print("🚀 Pipeline Pronta! Todos os componentes estão operacionais.")
        return True

if __name__ == "__main__":
    check_environment()
