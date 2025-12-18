import pandas as pd
import numpy as np
import joblib
import json
import random

# Tentar importar sklearn, se falhar, usar modo fallback
try:
    from sklearn.model_selection import train_test_split
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.metrics import accuracy_score
    SKLEARN_AVAILABLE = True
except ImportError:
    print("AVISO: Scikit-learn não encontrado ou com erro. Usando modo simplificado (Mock Model).")
    SKLEARN_AVAILABLE = False

class MockChurnModel:
    def predict(self, X):
        # Lógica dummy baseada em médias observadas (heurística)
        preds = []
        for _, row in X.iterrows():
            prob = 0.2
            if row.get('avaliacao_conteudo', 5) < 3.0: prob += 0.4
            if row.get('tempo_assinatura_meses', 12) < 6: prob += 0.3
            preds.append(1 if prob > 0.5 else 0)
        return np.array(preds)
    
    def predict_proba(self, X):
        # Retorna probs simuladas
        preds = []
        for _, row in X.iterrows():
            prob = 0.2
            if row.get('avaliacao_conteudo', 5) < 3.0: prob += 0.4
            if row.get('tempo_assinatura_meses', 12) < 6: prob += 0.3
            preds.append([1-prob, prob]) # [prob_0, prob_1]
        return np.array(preds)

def run_pipeline():
    global SKLEARN_AVAILABLE
    print("Iniciando pipeline de Churn...")
    
    # 1. Carregar dados
    try:
        df = pd.read_csv('dataset_churn_streaming_3000_registros.csv')
        print(f"Dados carregados. Shape: {df.shape}")
    except FileNotFoundError:
        print("Erro: Arquivo csv não encontrado.")
        return

    # 2. Limpeza Básica
    if 'cliente_id' in df.columns:
        df = df.drop(columns=['cliente_id'])

    text_cols = ['plano_assinatura', 'metodo_pagamento', 'dispositivo_principal']
    
    for col in df.columns:
        if df[col].dtype == 'object':
            mode_val = df[col].mode()[0]
            df[col] = df[col].fillna(mode_val)
        else:
            mean_val = df[col].mean()
            df[col] = df[col].fillna(mean_val)

    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.lower().str.strip()

    # Mapeamentos simplificados
    if 'plano_assinatura' in df.columns:
        df['plano_assinatura'] = df['plano_assinatura'].replace({'básico': 'basico', 'padrão': 'padrao'})
    
    if 'metodo_pagamento' in df.columns:
        df['metodo_pagamento'] = df['metodo_pagamento'].replace({'cartão de crédito': 'credito', 'cartao de credito': 'credito'})

    # 3. Encoding Manual Simples (para não depender de get_dummies complicado no backend depois)
    # Vamos apenas converter colunas categóricas para códigos numéricos simples para este MVP
    mappings = {}
    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].astype('category')
            mappings[col] = dict(enumerate(df[col].cat.categories))
            df[col] = df[col].cat.codes

    print("Limpeza concluída.")

    X = df.drop(columns=['churn'])
    y = df['churn']

    model = None
    
    if SKLEARN_AVAILABLE:
        try:
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            model = RandomForestClassifier(n_estimators=100, random_state=42)
            model.fit(X_train, y_train)
            acc = accuracy_score(y_test, model.predict(X_test))
            print(f"Modelo RandomForest treinado. Acurácia: {acc:.4f}")
        except Exception as e:
            print(f"Erro ao usar sklearn: {e}. Indo para fallback.")
            SKLEARN_AVAILABLE = False

    if not SKLEARN_AVAILABLE:
        # Criar um Mock Model simples que segue a lógica básica dos dados
        # Ex: Clientes com avaliação baixa ou tempo curto têm mais chance de churn
        print("Treinando Mock Model (Regras Baseadas em Dados)...")
        model = MockChurnModel()
        print("Mock Model 'treinado'.")

    # 4. Salvar Modelo e Artefatos
    joblib.dump(model, 'churn_model.joblib')
    
    # Salvar metadados das colunas necessárias
    with open('model_metadata.json', 'w') as f:
        json.dump({
            'columns': X.columns.tolist(),
            'mappings': mappings,
            'model_type': 'sklearn' if SKLEARN_AVAILABLE else 'mock'
        }, f)

    print("Pipeline finalizado com sucesso. Modelo e metadados salvos.")

if __name__ == "__main__":
    run_pipeline()
