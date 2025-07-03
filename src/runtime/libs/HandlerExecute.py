import time
from runtime.libs.HandlerCallback import HandlerCallback
from runtime.context import create_context
from runtime.libs.log import write

class HandlerExecute:
    @staticmethod
    def handle(payload: dict, headers: dict) -> dict:
        try:
            handler = HandlerCallback.get(payload)
            context = create_context(headers)

            start_ns = time.perf_counter_ns()
            result = handler(payload, context)
            end_ns = time.perf_counter_ns()

            duration_ms = (end_ns - start_ns) / 1_000_000
            write(f"⏱️ Handler executed in {duration_ms:.2f} ms")

            # Assegura que o resultado é um dict (formato esperado pelo Lambda)
            return result if isinstance(result, dict) else {"result": result}

        except Exception as e:
            write(f"⚠️ Handler execution failed: {str(e)}")
            # Para falhas em batch (ex: SQS) retorna lista vazia para reprocessamento
            return {"batchItemFailures": []}

