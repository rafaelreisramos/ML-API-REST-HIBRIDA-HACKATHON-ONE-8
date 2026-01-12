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

# Tentar carregar Modelo G8 (Prioridade Total)
MODEL_DIR = os.path.join(os.path.dirname(__file__), 'models')
MODEL_PATH = os.path.join(MODEL_DIR, 'modelo_churn.joblib')
THRESHOLD_PATH = os.path.join(MODEL_DIR, 'threshold_otimo.txt')

# Mock de Emergência
class MockChurnModelV4:
    def predict(self, df):
        return [1] if df.iloc[0].get('avaliacao_conteudo_media', 5) < 3 else [0]
    
    def predict_proba(self, df):
        p = 0.8 if df.iloc[0].get('avaliacao_conteudo_media', 5) < 3 else 0.2
        return [[1-p, p]]

try:
    model = joblib.load(MODEL_PATH)
    print(f"✅ [AI SERVICE] Modelo G8 carregado: {MODEL_PATH}")
    
    with open(THRESHOLD_PATH, 'r') as f:
        threshold_otimo = float(f.read().strip())
    print(f"✅ [AI SERVICE] Threshold Otimizado: {threshold_otimo}")
    
except Exception as e:
    print(f"❌ [AI SERVICE] FALHA CRÍTICA ao carregar modelo G8: {e}")
    # Fallback apenas para não crashar o container, mas a predição será dummy
    model = MockChurnModelV4()
    threshold_otimo = 0.5

# Modelo de Entrada Atualizado (Compatível com ChurnData.java)
class JavaInput(BaseModel):
    # Campos V1 (Legado mantido por segurança)
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
    
    # Novos campos Obrigatórios V8 (Hackathon G8)
    tipoContrato: str
    categoriaFavorita: str
    acessibilidade: int # 0 ou 1

@app.post("/predict")
def predict(input_data: JavaInput):
    if not model:
        raise HTTPException(status_code=500, detail="Modelo offline")
        
    try:
        data = input_data.model_dump()
        
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
            "acessibilidade": "acessibilidade",
            "regiao": "regiao",
            "genero": "genero",
            "idade": "idade"
        }
        
        row = {}
        for java_k, py_k in mapper.items():
            if java_k in data:
                row[py_k] = data[java_k]
                
        df = pd.DataFrame([row])
        
        # --- Preprocessamento Híbrido V8 ---
        from processing import preprocess_input
        df = preprocess_input(df)
        
        # Previsão
        probabilidade = 0.0
        prediction = 0
        
        if hasattr(model, 'predict_proba'):
            try:
                # O modelo espera features selecionadas pelo RFE (já feito no preprocess)
                probs = model.predict_proba(df)
                probabilidade = float(probs[0][1])
                
                # Decisão usando Threshold Otimizado (G8)
                prediction = 1 if probabilidade > threshold_otimo else 0
                
            except ValueError as ve:
                print(f"❌ Erro de predição: {ve}")
                raise ve
        else:
            prediction = model.predict(df)[0]
            probabilidade = 0.9 if prediction == 1 else 0.1
            
        return {
            "previsao": "Vai cancelar" if int(prediction) == 1 else "Vai continuar",
            "probabilidade": round(probabilidade, 4),
            "riscoAlto": bool(probabilidade > 0.6), # Regra de negócio extra
            "modeloUsado": f"RandomForest G8 (Threshold: {threshold_otimo})"
        }
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
