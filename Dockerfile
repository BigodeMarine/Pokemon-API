# Imagem oficial do Python
FROM python:3.11-slim

# Evita geração de arquivos .pyc
ENV PYTHONDONTWRITEBYTECODE=1

# Exibe logs imediatamente
ENV PYTHONUNBUFFERED=1

# Diretório de trabalho dentro do container
WORKDIR /app

# Copia apenas as dependências primeiro
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do projeto
COPY . .

# Porta utilizada pela API
EXPOSE 8000

# Inicializa a aplicação
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]