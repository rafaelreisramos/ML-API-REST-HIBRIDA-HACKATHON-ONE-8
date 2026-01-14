FROM python:3.11-slim

WORKDIR /app

# Instalar dependências de sistema se necessário (opcional)
# RUN apt-get update && apt-get install -y gcc

# Copiar requirements primeiro para cache do Docker
COPY ai_service/requirements.txt .

# Instalar bibliotecas Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código fonte do AI Service
COPY ai_service/server.py ai_service/train_model.py ai_service/processing.py ./

# Criar diretório de modelos
RUN mkdir -p /app/models

# Copiar artefatos do modelo do time de Data Science
# Estes arquivos são necessários para o Auto-Healing funcionar
COPY hackathon_g8_one/data/X_train.csv /app/models/
COPY hackathon_g8_one/data/y_train.csv /app/models/
COPY hackathon_g8_one/models/rfe_selector.joblib /app/models/
COPY hackathon_g8_one/models/threshold_otimo.txt /app/models/
COPY hackathon_g8_one/models/features_selecionadas_rfe.csv /app/models/
COPY hackathon_g8_one/models/label_encoders_g8.json /app/models/

# Copiar o modelo treinado (quando disponível do time de DS)
# COPY hackathon_g8_one/models/modelo_churn.joblib /app/models/

# Expor a porta 5000
EXPOSE 5000

# Healthcheck para Kubernetes/OCI
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000/docs')" || exit 1

# Comando para rodar o servidor
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "5000"]
