import joblib
import pandas as pd
import os
import sys

# Hack para MockChurnModel ser encontrado se necessario
try:
    import train_model
    sys.modules['__main__'].MockChurnModel = train_model.MockChurnModel
except ImportError:
    pass

def analyze():
    try:
        print("Iniciando analise DENTRO DO CONTAINER...")
        
        # Caminhos no container
        model_path = os.path.join('models', 'modelo_churn.joblib')
        features_path = os.path.join('models', 'features_selecionadas_rfe.csv')
        
        if not os.path.exists(model_path):
            print(f"Erro: Modelo nao encontrado em {model_path}")
            return

        model = joblib.load(model_path)
        features_df = pd.read_csv(features_path)
        feature_names = features_df['feature'].tolist()
        
        if hasattr(model, 'feature_importances_'):
            importances = model.feature_importances_
            
            # Ajuste de tamanho se necessario
            length = min(len(importances), len(feature_names))
            
            df_imp = pd.DataFrame({
                'feature': feature_names[:length],
                'importance': importances[:length]
            })
            
            df_imp = df_imp.sort_values(by='importance', ascending=False)
            
            print("\n" + "="*40)
            print(" TOP FEATURES (RandomForest G8)")
            print("="*40)
            for i, row in df_imp.head(15).iterrows():
                print(f"{i+1:02d}. {row['feature']:<30} | {row['importance']:.4f}")
            print("="*40)
        else:
            print(f"Modelo sem feature_importances_. Tipo: {type(model)}")
            print(f"Atributos disponiveis: {dir(model)}")
            
            # Tentar acessar best_estimator se for grid search / pipeline
            if hasattr(model, 'best_estimator_'):
                print("Tentando acessar best_estimator_...")
                model = model.best_estimator_
                print(f"Novo tipo: {type(model)}")
                if hasattr(model, 'feature_importances_'):
                    importances = model.feature_importances_
                    # (Repetir logica de print - simplificada aqui)
                    length = min(len(importances), len(feature_names))
                    df_imp = pd.DataFrame({'feature': feature_names[:length], 'importance': importances[:length]}).sort_values('importance', ascending=False)
            # Tratamento para CalibratedClassifierCV
            elif type(model).__name__ == 'CalibratedClassifierCV':
                print("Detectado CalibratedClassifierCV. Tentando extrair base_estimator...")
                base_model = None
                
                # Caso 1: Se foi treinado com cv='prefit' ou tem estimator exposto
                if hasattr(model, 'estimator'):
                    base_model = model.estimator
                # Caso 2: Se tem varios classificadores, pegar o primeiro (media seria melhor mas pro MVP serve)
                elif hasattr(model, 'calibrated_classifiers_') and len(model.calibrated_classifiers_) > 0:
                    base_model = model.calibrated_classifiers_[0].estimator
                
                if base_model and hasattr(base_model, 'feature_importances_'):
                    importances = base_model.feature_importances_
                    length = min(len(importances), len(feature_names))
                    df_imp = pd.DataFrame({'feature': feature_names[:length], 'importance': importances[:length]}).sort_values('importance', ascending=False)
                    print("\n=== TOP FEATURES (VIA CALIBRATED BASE MODEL) ===")
                    for i, row in df_imp.head(15).iterrows():
                        print(f"{i+1:02d}. {row['feature']:<30} | {row['importance']:.4f}")
                    print("="*40)
                else:
                    print(f"Nao foi possivel extrair feature_importances_ do base_model: {type(base_model)}")

    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    analyze()
