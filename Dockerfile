# Use a imagem base do Python
FROM python:3.12-slim

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos de dependências do worker
COPY src/requirements.txt .

# Instala as dependências do worker
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código do worker
COPY src/bua /app/bua

# Comando para iniciar o worker do Temporal
CMD ["python", "-m", "bua.temporal.worker"]
