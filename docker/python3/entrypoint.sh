#!/bin/sh

export PYTHONPATH=/var/task

if [ "$LAMBDA_ENV" = "dev" ]; then
    echo "🚀 Modo Desenvolvimento: iniciando main.py para testes locais"
    exec python3 /var/task/main.py
else
    echo "⚙️ Modo Produção: iniciando runtime oficial AWS Lambda"
    exec /var/runtime/bootstrap
fi

