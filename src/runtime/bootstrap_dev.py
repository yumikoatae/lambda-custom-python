import json
import sys
import os

# 🔧 Garante que o Python enxergue o diretório onde está o main.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main import handler
from runtime.context import get_context

# Evento simulado (troque conforme o que quiser testar)
event = {
    "httpMethod": "GET",
    "path": "/test"
}

# Ou simule SQS:
# event = {
#     "Records": [{"body": "msg 1"}, {"body": "msg 2"}]
# }

context = get_context()
response = handler(event, context)
print(json.dumps(response, indent=2))

