#!/bin/sh

# Espera o MySQL ficar pronto
echo "Aguardando o banco de dados ficar pronto..."

while ! nc -z db 3306; do
  sleep 1
done

echo "Banco de dados está pronto!"

# Agora roda o comando original que o container executaria
exec "$@"
