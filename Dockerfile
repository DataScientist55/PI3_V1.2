# Usar uma imagem base do Python
FROM python:3.12

# Copiar o arquivo de dependências para o contêiner
COPY requirements.txt /app/

# Instalar dependências para compilar o mysqlclient
RUN apt-get update && apt-get install -y \
    pkg-config \
    default-libmysqlclient-dev \
    build-essential \
    libssl-dev \
    libffi-dev
RUN pip install --upgrade pip
#RUN pip install -r requirements.txt

# Definir o diretório de trabalho no contêiner
WORKDIR /app

# Instalar as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código do projeto para dentro do contêiner
COPY . /app/

# Expor a porta 8000 para o servidor Django
EXPOSE 8000

# Comando para rodar o servidor Django
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
CMD ["gunicorn", "EstEsc.wsgi:application", "--bind", "0.0.0.0:8000"]