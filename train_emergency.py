import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

print("🚀 Iniciando Treinamento de Emergência...")

# Caminhos
BASE_DIR = 'hackathon_g8_one/data'
MODEL_DIR = 'ai_service/models'

X_train_path = os.path.join(BASE_DIR, 'X_train.csv')
y_train_path = os.path.join(BASE_DIR, 'y_train.csv')
output_model_path = os.path.join(MODEL_DIR, 'modelo_churn.joblib')

# Carregar Dados
print(f"📂 Carregando dados de: {BASE_DIR}")
X_train = pd.read_csv(X_train_path)
y_train = pd.read_csv(y_train_path)

# Ajustar y se necessário (ravel)
if y_train.shape[1] == 1:
    y_train = y_train.iloc[:, 0]

print(f"📊 Dados carregados: X={X_train.shape}, y={y_train.shape}")

# Treinar Modelo (Random Forest similar ao original)
print("🧠 Treinando RandomForestClassifier...")
# Usando hiperparâmetros 'padrão' robustos, já que não lemos o CSV de hiperparams
clf = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10)
clf.fit(X_train, y_train)

# Salvar
print(f"💾 Salvando modelo em: {output_model_path}")
joblib.dump(clf, output_model_path)

print("✅ Modelo reconstruído com sucesso!")
