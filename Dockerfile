# Usar uma imagem base do Python
FROM python:3.12-slim

# Copiar o arquivo de dependências para o contêiner
COPY requirements.txt /app/

# Instalar dependências para compilar o mysqlclient
RUN apt-get update && apt-get install -y netcat-traditional pkg-config default-libmysqlclient-dev build-essential libssl-dev libffi-dev


# Atualizar o pip
RUN pip install --upgrade pip

# Instalar as dependências do projeto
RUN pip install -r /app/requirements.txt

# Definir o diretório de trabalho no contêiner
WORKDIR /app

# Copiar o código do projeto para dentro do contêiner
COPY . /app/

# Expor a porta 8000 para o servidor Django
EXPOSE 8000

# Comando para rodar o servidor Django com Gunicorn
CMD ["gunicorn", "EstEsc.wsgi:application", "--bind", "0.0.0.0:8000"]
