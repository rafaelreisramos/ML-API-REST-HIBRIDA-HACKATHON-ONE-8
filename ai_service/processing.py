import pandas as pd
import json

# Carregar metadados uma vez
try:
    with open('model_metadata.json', 'r') as f:
        metadata = json.load(f)
        
    mappings = metadata.get('mappings', {})
    reversed_mappings = {}
    for col, map_dict in mappings.items():
        reversed_mappings[col] = {v: int(k) for k, v in map_dict.items()}
except Exception as e:
    print(f"Erro ao carregar metadados: {e}")
    metadata = {}
    reversed_mappings = {}

def preprocess_input(df_input: pd.DataFrame):
    """Aplica as mesmas transformações do treino no dataframe de entrada."""
    text_cols = ['plano_assinatura', 'metodo_pagamento', 'dispositivo_principal']
    
    # Cópia para não alterar original se for view
    df_proc = df_input.copy()

    # Normalização de Texto
    for col in text_cols:
        if col in df_proc.columns:
            df_proc[col] = df_proc[col].astype(str).str.lower().str.strip()
            
            # Correções manuais
            if col == 'plano_assinatura':
                df_proc[col] = df_proc[col].replace({'básico': 'basico', 'padrão': 'padrao'})
            if col == 'metodo_pagamento':
                df_proc[col] = df_proc[col].replace({'cartão de crédito': 'credito', 'cartao de credito': 'credito'})

    # Encoding (Converter Texto -> Número)
    for col, mapping in reversed_mappings.items():
        if col in df_proc.columns:
            # Map com valor default 0 para desconhecidos
            df_proc[col] = df_proc[col].map(mapping).fillna(0).astype(int)

    # Garantir colunas esperadas pelo modelo
    if 'columns' in metadata:
        expected_cols = metadata['columns']
        for col in expected_cols:
            if col not in df_proc.columns:
                df_proc[col] = 0
        df_proc = df_proc[expected_cols]
    
    return df_proc
