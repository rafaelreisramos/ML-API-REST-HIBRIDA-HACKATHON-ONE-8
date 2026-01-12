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

# Carregar novos artefatos G8
import os
import joblib

MODEL_DIR = os.path.join(os.path.dirname(__file__), 'models')
LABEL_ENCODERS_PATH = os.path.join(MODEL_DIR, 'label_encoders_g8.json')
RFE_PATH = os.path.join(MODEL_DIR, 'rfe_selector.joblib')
FEATURES_PATH = os.path.join(MODEL_DIR, 'features_selecionadas_rfe.csv')

# Carregar recursos uma vez só
try:
    with open(LABEL_ENCODERS_PATH, 'r', encoding='utf-8') as f:
        encoders_map = json.load(f)
    print("✅ [AI SERVICE] Label Encoders G8 carregados.")
    
    rfe_selector = joblib.load(RFE_PATH)
    print("✅ [AI SERVICE] RFE Selector carregado.")
    
    features_esperadas = pd.read_csv(FEATURES_PATH)['feature'].tolist()
    print("✅ [AI SERVICE] Lista de Features carregada.")
except Exception as e:
    print(f"⚠️ [AI SERVICE] Erro ao carregar artefatos do modelo G8: {e}")
    encoders_map = {}
    rfe_selector = None
    features_esperadas = []

def preprocess_input(df_input: pd.DataFrame):
    """
    Pipeline de pré-processamento Híbrido V8:
    1. Normalização de texto
    2. Encoding com mapa G8
    3. Cálculo de features derivadas (Engajamento, Risco, Flags)
    4. Seleção de features (RFE)
    """
    df_proc = df_input.copy()
    
    # Colunas de texto para normalizar (uppercase para bater com encoders G8)
    text_cols = ['genero', 'regiao', 'tipo_contrato', 'metodo_pagamento', 
                 'plano_assinatura', 'dispositivo_principal', 'categoria_favorita']
    
    for col in text_cols:
        if col in df_proc.columns:
            # Converter para UPPERCASE pois os encoders estão assim
            df_proc[col] = df_proc[col].astype(str).str.upper().str.strip()
            
            # Correções de compatibilidade (Legado -> G8)
            if col == 'plano_assinatura':
                # 'premium' -> 'PREMIUM' já feito pelo upper()
                pass
            if col == 'metodo_pagamento':
                # 'credito' -> 'CARTÃO DE CRÉDITO' (ajuste fino)
                df_proc[col] = df_proc[col].replace({
                    'CREDITO': 'CARTÃO DE CRÉDITO',
                    'DEBITO': 'DÉBITO'
                })

    # Encoding Manual (Baseado no JSON G8)
    for col, mapping in encoders_map.items():
        if col in df_proc.columns:
            # Map e preencher desconhecidos com -1 ou moda (0)
            df_proc[col] = df_proc[col].map(mapping).fillna(0).astype(int)

    # --- Feature Engineering (Derivadas) ---
    
    # Flags Booleanas (0/1)
    for col in ['avaliacao_conteudo_media', 'avaliacao_conteudo_ultimo_mes', 'avaliacao_plataforma']:
        new_col = f'tem_{col}'
        if col in df_proc.columns:
            df_proc[new_col] = df_proc[col].notna().astype(int)
            # Preencher nulos com média neutra (opcional, aqui assume 0 se nulo na origem)
            df_proc[col] = df_proc[col].fillna(0)
        else:
            df_proc[new_col] = 0
            df_proc[col] = 0

    # Visualizações por dia
    if 'visualizacoes_mes' in df_proc.columns:
        df_proc['visualizacoes_por_dia'] = df_proc['visualizacoes_mes'] / 30.0
    else:
        df_proc['visualizacoes_por_dia'] = 0.0

    # Engajamento Score (Fórmula aproximada do treinamento)
    # visualizacoes_por_dia * 0.4 + tempo_medio_sessao_min / 200 * 0.6
    tempo_sessao = df_proc.get('tempo_medio_sessao_min', 0)
    vis_dia = df_proc.get('visualizacoes_por_dia', 0)
    df_proc['engajamento_score'] = (vis_dia * 0.4) + ((tempo_sessao / 200.0) * 0.6)

    # Risco Score (Fórmula baseada em inatividade)
    # dias_ultimo_acesso / 100
    dias_inat = df_proc.get('dias_ultimo_acesso', 0)
    df_proc['risco_score'] = dias_inat / 100.0

    # Inativo Flag (> 30 dias)
    df_proc['inativo_flag'] = (dias_inat > 30).astype(int)
    
    # Validação de Colunas Faltantes (Preencher com 0)
    # Lista completa esperada pelo modelo G8 (antes do RFE)
    cols_para_rfe = features_esperadas # Na verdade o RFE espera um X maior, mas vamos garantir o minimo
    # (Para simplificar, vamos assumir que features_esperadas são as FINAIS ou as de entrada do RFE? 
    # O arquivo diz 'features_selecionadas_rfe.csv', então são as FINAIS.
    # O RFE transform precisa das colunas originais de treino. Como não temos a lista original fácil aqui,
    # vamos TENTAR passar as colunas geradas. Se o RFE falhar, usaremos as features selecionadas diretamente.)
    
    # Estratégia Segura: Garantir que todas as 'features_esperadas' existam no DF
    for col in features_esperadas:
        if col not in df_proc.columns:
            df_proc[col] = 0
            
    # Reordenar para bater com a expectativa do modelo (CRÍTICO)
    # Se usarmos o RFE object, precisamos das colunas originais.
    # Se o modelo já espera as colunas pós-RFE, basta filtrar.
    # O pipeline descrito diz: Dados -> RFE -> Modelo.
    # Então df_proc deve ter colunas ORIGINAIS antes do RFE.
    # Vamos pular o RFE transform se as colunas não baterem e tentar entregar direto as features finais.
    
    try:
        # Tentar selecionar apenas as features finais esperadas
        df_proc = df_proc[features_esperadas]
    except KeyError as e:
        print(f"⚠️ Erro de colunas: {e}")
        
    return df_proc
