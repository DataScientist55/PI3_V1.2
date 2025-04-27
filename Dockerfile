FROM python:3.12.10-slim

# Instala as dependências necessárias
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos do projeto para o contêiner
COPY . /app

# Instala as dependências do projeto
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Executa as migrações e coleta os arquivos estáticos
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput

# Expõe a porta que o Railway utiliza
EXPOSE 8000

# Comando para iniciar a aplicação
CMD ["gunicorn", "EstEsc.wsgi:application", "--bind", "0.0.0.0:8000"]
