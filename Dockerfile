FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y \
    libmysqlclient-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*


# Apenas coleta os estáticos (não faz migrate no build)
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "seuprojeto.wsgi:application", "--bind", "0.0.0.0:8000"]
