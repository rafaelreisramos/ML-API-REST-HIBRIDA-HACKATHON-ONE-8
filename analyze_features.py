import joblib
import pandas as pd
import os

def analyze():
    try:
        print("Iniciando analise de importancia das features...")
        
        # Caminhos relativos a raiz do projeto
        model_path = os.path.join('hackathon_g8_one', 'models', 'modelo_churn.joblib')
        features_path = os.path.join('hackathon_g8_one', 'models', 'features_selecionadas_rfe.csv')
        
        if not os.path.exists(model_path):
            print(f"Erro: Modelo n nao encontrado em {model_path}")
            return

        print(f"Carregando modelo de {model_path}...")
        model = joblib.load(model_path)
        print("Modelo carregado com sucesso.")

        print(f"Lendo nomes das features de {features_path}...")
        features_df = pd.read_csv(features_path)
        feature_names = features_df['feature'].tolist()
        
        # Validar tamanhos
        if hasattr(model, 'feature_importances_'):
            importances = model.feature_importances_
            
            if len(importances) != len(feature_names):
                print(f"AVISO: Numero de features no modelo ({len(importances)}) diferente do CSV ({len(feature_names)})")
                # Tentar ajustar se possivel, ou apenas mostrar os primeiros
                length = min(len(importances), len(feature_names))
                importances = importances[:length]
                feature_names = feature_names[:length]

            # Criar DataFrame
            df_imp = pd.DataFrame({
                'feature': feature_names,
                'importance': importances
            })
            
            # Ordenar
            df_imp = df_imp.sort_values(by='importance', ascending=False)
            
            print("\n" + "="*40)
            print(" TOP 10 FEATURES MAIS IMPORTANTES (CHURN)")
            print("="*40)
            
            # Formatar para exibição
            for i, row in df_imp.head(15).iterrows():
                print(f"{i+1:02d}. {row['feature']:<30} | {row['importance']:.4f}")
                
            print("="*40)
            
        else:
            print("O modelo carregado nao possui o atributo 'feature_importances_'.")
            print(f"Tipo do modelo: {type(model)}")

    except Exception as e:
        print(f"Ocorreu um erro durante a analise: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    analyze()
