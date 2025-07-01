#!/bin/sh

export PYTHONPATH=/var/task:$PYTHONPATH

if [ "$LAMBDA_ENV" = "dev" ]; then
  echo "🔧 Iniciando em modo DEV..."
  exec python3 /var/task/server.py
else
  echo "🚀 Iniciando em modo PROD (AWS Lambda)..."
  exec /var/runtime/bootstrap
fi

