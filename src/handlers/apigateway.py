import json
import time
from werkzeug.test import EnvironBuilder
from werkzeug.wrappers import Request
from werkzeug.exceptions import HTTPException
from runtime.libs.log import write
from server import server  # seu app WSGI

def handler(event: dict, context: dict) -> dict:
    """
    Handler Lambda que converte evento API Gateway em requisição WSGI,
    despacha para seu app e retorna resposta formatada para AWS Lambda.

    Serve para rodar local (com evento simulado) ou na produção AWS Lambda container.
    """
    try:
        start = time.perf_counter()
        write(json.dumps(event, ensure_ascii=False))

        # Extrai informações do evento para criar request WSGI
        method = event.get("httpMethod") or event.get("requestContext", {}).get("http", {}).get("method", "GET")
        path = event.get("path") or event.get("rawPath", "/")
        headers = event.get("headers") or {}
        body = event.get("body") or ""
        query = event.get("queryStringParameters") or {}

        # Monta ambiente WSGI simulando uma requisição HTTP
        builder = EnvironBuilder(
            method=method,
            path=path,
            headers=headers,
            data=body.encode("utf-8") if isinstance(body, str) else body,
            query_string=query
        )
        env = builder.get_environ()
        request = Request(env)

        # Despacha para seu app WSGI (server.py)
        response = server.dispatch_request(request)

        # Se for exceção HTTP, transforma em response
        if isinstance(response, HTTPException):
            response = response.get_response(env)

        # Lê o corpo da resposta (bytes)
        body_bytes = b"".join(response.iter_encoded()) if hasattr(response, "iter_encoded") else b"".join(iter(response))

        end = time.perf_counter()
        write(f"⏱️ Tempo total: {(end - start)*1000:.2f}ms")

        # Retorna formato esperado pelo Lambda
        return {
            "statusCode": response.status_code,
            "headers": dict(response.headers),
            "body": body_bytes.decode("utf-8")
        }

    except Exception as e:
        write(f"❌ Erro no handler: {e}")
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": "Erro interno"})
        }

