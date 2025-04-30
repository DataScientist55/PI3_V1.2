# Imagem base do Python
FROM python:3.12-slim

# Evita prompts interativos durante a instalação
ENV DEBIAN_FRONTEND=noninteractive

# Criar diretório de trabalho
WORKDIR /app

# Copiar o arquivo de dependências
COPY requirements.txt .

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    netcat-traditional \
    pkg-config \
    default-libmysqlclient-dev \
    build-essential \
    libssl-dev \
    libffi-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Instalar pip e as dependências do projeto
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copiar o restante do projeto para dentro do contêiner
COPY . .

# Coleta arquivos estáticos automaticamente na imagem
RUN python manage.py collectstatic --noinput

# Expõe a porta usada pelo Gunicorn
EXPOSE 8000

# Comando para iniciar o Gunicorn
CMD ["gunicorn", "EstEsc.wsgi:application", "--bind", "0.0.0.0:8000"]
