FROM python:3.10-slim

WORKDIR /app

# Instalar dependências de sistema se necessário (opcional)
# RUN apt-get update && apt-get install -y gcc

# Copiar requirements primeiro para cache do Docker
COPY requirements.txt .

# Instalar bibliotecas Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o restante dos arquivos do projeto
COPY . .

# Expor a porta 5000
EXPOSE 5000

# Comando para rodar o servidor
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "5000"]
