FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Apenas coleta os estáticos (não faz migrate no build)
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "seuprojeto.wsgi:application", "--bind", "0.0.0.0:8000"]
