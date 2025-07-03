import time
import random
from runtime.libs.log import write

def handler(event: dict, context: dict) -> dict:
    """
    Handler para processar eventos do SQS.

    - Recebe lote de mensagens em 'Records'.
    - Processa cada registro com controle de timeout.
    - Retorna falhas para evitar reprocessamento.
    - Funciona local e em Lambda AWS.
    """
    try:
        records = event.get("Records", [])
        if not records:
            write("⚠️ Nenhum registro SQS recebido.")
            return {"batchItemFailures": []}

        write(f"🧮 Processando lote com {len(records)} registros")

        # Tempo restante para executar a função, para evitar timeout
        total_timeout_ms = context.get("getRemainingTimeInMillis", lambda: 30000)()
        # Definindo margem para parar processamento antes do timeout real
        MARGIN_PCT = 0.15
        MIN_MARGIN_MS = 2000
        margin_ms = max(MIN_MARGIN_MS, total_timeout_ms * MARGIN_PCT)
        deadline = int(time.time() * 1000) + total_timeout_ms - margin_ms

        failures = []
        processed = 0
        total_time_ms = 0

        for record in records:
            remaining_ms = deadline - int(time.time() * 1000)
            avg_time_ms = (total_time_ms / processed) if processed else 0

            # Para evitar timeout, interrompe processamento se tempo insuficiente
            if processed > 0 and remaining_ms < avg_time_ms:
                write(f"⏳ Tempo insuficiente para processar {record.get('messageId')}, pulando.")
                failures.append({"itemIdentifier": record.get("messageId")})
                continue

            try:
                write(f"📨 Processando mensagem {record.get('messageId')}")
                write(f"📝 Corpo: {record.get('body')}")

                start_ms = int(time.time() * 1000)
                process_record(record)
                elapsed_ms = int(time.time() * 1000) - start_ms

                total_time_ms += elapsed_ms
                processed += 1

            except Exception as e:
                write(f"❌ Erro ao processar {record.get('messageId')}: {e}")
                failures.append({"itemIdentifier": record.get("messageId")})

        write(f"✅ Processados {processed} de {len(records)} registros")
        return {"batchItemFailures": failures}

    except Exception as err:
        write(f"❌ Erro fatal no handler SQS: {err}")
        return {"batchItemFailures": []}

def process_record(record: dict) -> None:
    """
    Função mock de processamento. Ajuste aqui para sua lógica real.
    """
    # Exemplo: erro proposital se corpo contém 'fail'
    if "fail" in record.get("body", ""):
        raise Exception("Erro simulado")

    # Simula tempo de processamento (300-400 ms)
    time.sleep(0.3 + random.uniform(0, 0.1))

