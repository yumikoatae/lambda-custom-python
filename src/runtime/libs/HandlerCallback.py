import os
from typing import Callable

class HandlerCallback:
    _handlers_cache: dict[str, Callable] = {}

    @staticmethod
    def get(payload: dict) -> Callable:
        """
        Retorna a função handler correta conforme o payload recebido.
        Faz cache para não carregar toda vez.
        """
        # Corrigido: base aponta para 'src' (2 níveis acima de libs)
        base = os.getenv("LAMBDA_TASK_ROOT") or os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
        
        handler_path = HandlerCallback._select_handler_path(payload, base)

        if not os.path.isfile(handler_path):
            raise FileNotFoundError(f"Handler file not found: {handler_path}")

        if handler_path not in HandlerCallback._handlers_cache:
            namespace = {}
            with open(handler_path, "r", encoding="utf-8") as f:
                code = compile(f.read(), handler_path, "exec")
                exec(code, namespace)

            handler_func = namespace.get("handler")
            if not callable(handler_func):
                raise Exception(f"No callable 'handler' found in {handler_path}")

            HandlerCallback._handlers_cache[handler_path] = handler_func

        return HandlerCallback._handlers_cache[handler_path]

    @staticmethod
    def _select_handler_path(payload: dict, base_path: str) -> str:
        """
        Detecta o tipo do evento pelo payload e retorna o caminho do handler correto.
        """
        if "Records" in payload:
            return os.path.join(base_path, "handlers", "sqs.py")

        if "rawPath" in payload:
            return os.path.join(base_path, "handlers", "apigateway.py")

        # Adicione aqui outros tipos de eventos conforme seu projeto

        # Default handler genérico
        return os.path.join(base_path, "handlers", "generic.py")

