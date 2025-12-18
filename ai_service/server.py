import joblib
import pandas as pd
import uvicorn
from fastapi import FastAPI, HTTPException
import sys
import os
import json
from pydantic import BaseModel

# --- Mapeamento de Contexto para Pickle ---
sys.path.append(os.getcwd())
try:
    from train_model import MockChurnModel
    sys.modules['__main__'].MockChurnModel = MockChurnModel
except ImportError:
    pass
# ------------------------------------------

app = FastAPI(title="AI Churn Service V4", description="Microserviço Python para inferência de modelo V4")

# Tentar carregar V4, senão V1
MODEL_PATH = 'churn_model_v4.joblib'
if not os.path.exists(MODEL_PATH):
    MODEL_PATH = 'churn_model.joblib'

class MockChurnModelV4:
    def predict(self, df):
        return [1] if df.iloc[0].get('avaliacao_conteudo_media', 5) < 3 else [0]
    
    def predict_proba(self, df):
        p = 0.8 if df.iloc[0].get('avaliacao_conteudo_media', 5) < 3 else 0.2
        return [[1-p, p]]

try:
    model = joblib.load(MODEL_PATH)
    print(f"✅ [AI SERVICE] Modelo '{MODEL_PATH}' carregado com sucesso!")
except Exception as e:
    print(f"❌ [AI SERVICE] Erro ao carregar modelo '{MODEL_PATH}': {e}")
    print("⚠️ [AI SERVICE] Ativando Mock Model V4 de Emergência")
    model = MockChurnModelV4()
    MODEL_PATH = "MOCK-V4-EMERGENCY"

# Modelo de Entrada (Superset V1 + V4)
class JavaInput(BaseModel):
    # Campos V1 (Legado)
    idade: int
    tempoAssinaturaMeses: int
    planoAssinatura: str
    valorMensal: float
    visualizacoesMes: int
    contatosSuporte: int
    metodoPagamento: str
    dispositivoPrincipal: str
    
    # Campos V4
    avaliacaoConteudoMedia: float
    avaliacaoConteudoUltimoMes: float
    tempoMedioSessaoMin: int
    diasUltimoAcesso: int
    avaliacaoPlataforma: float
    regiao: str
    genero: str
    
    # Novos campos potenciais V4 (opcionais por enquanto)
    tipoContrato: str | None = "Mensal"
    categoriaFavorita: str | None = "Geral"

@app.post("/predict")
def predict(input_data: JavaInput):
    if not model:
        raise HTTPException(status_code=500, detail="Modelo offline")
        
    try:
        data = input_data.dict()
        
        # --- Mapper Universal (Java -> Python Snake Case) ---
        mapper = {
            "tempoAssinaturaMeses": "tempo_assinatura_meses",
            "planoAssinatura": "plano_assinatura",
            "valorMensal": "valor_mensal",
            "visualizacoesMes": "visualizacoes_mes",
            "contatosSuporte": "contatos_suporte",
            "metodoPagamento": "metodo_pagamento",
            "dispositivoPrincipal": "dispositivo_principal",
            "avaliacaoConteudoMedia": "avaliacao_conteudo_media",
            "avaliacaoConteudoUltimoMes": "avaliacao_conteudo_ultimo_mes",
            "tempoMedioSessaoMin": "tempo_medio_sessao_min",
            "diasUltimoAcesso": "dias_ultimo_acesso",
            "avaliacaoPlataforma": "avaliacao_plataforma",
            "tipoContrato": "tipo_contrato",
            "categoriaFavorita": "categoria_favorita",
            "regiao": "regiao",
            "genero": "genero",
            "idade": "idade"
        }
        
        row = {}
        for java_k, py_k in mapper.items():
            if java_k in data:
                row[py_k] = data[java_k]
                
        df = pd.DataFrame([row])
        
        # --- Preprocessamento Dinâmico ---
        # Se for V4, provavelmente o pipeline já cuida do encoding.
        # Se for V1, precisamos do preprocess manual.
        # Vamos tentar inferir.
        
        is_pipeline = hasattr(model, 'steps') or hasattr(model, 'named_steps')
        
        if not is_pipeline and "model_v4" not in MODEL_PATH:
             # Fallback para V1 manual
             from processing import preprocess_input
             df = preprocess_input(df)
        
        # Garantir colunas faltantes com default 0/"" se o modelo exigir (via try/catch no predict)
             
        # Previsão
        probabilidade = 0.0
        prediction = 0
        
        if hasattr(model, 'predict_proba'):
            try:
                probs = model.predict_proba(df)
                probabilidade = float(probs[0][1])
                prediction = 1 if probabilidade > 0.5 else 0 # Threshold padrão
            except ValueError as ve:
                # Tentar one-hot encoding manual de emergencia se falhar (caso não seja pipeline)
                if "could not convert string to float" in str(ve):
                    print("⚠️ Erro de encoding. Tentando dummification simples...")
                    df = pd.get_dummies(df)
                    # Realign columns... (complexo para fazer on-the-fly)
                    raise ve
                raise ve
        else:
            prediction = model.predict(df)[0]
            probabilidade = 0.9 if prediction == 1 else 0.1
            
        return {
            "previsao": "Vai cancelar" if int(prediction) == 1 else "Vai continuar",
            "probabilidade": probabilidade,
            "riscoAlto": bool(probabilidade > 0.6),
            "modeloUsado": f"Python AI Service ({MODEL_PATH})"
        }
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
