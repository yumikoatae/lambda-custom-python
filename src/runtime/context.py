import os
import time
import uuid
from typing import Optional, Dict

def create_context(headers: Optional[Dict[str, str]] = None) -> dict:
    """
    Cria um contexto compatível com AWS Lambda.
    Funciona tanto localmente quanto dentro do Runtime API da AWS.
    """
    now_ms = lambda: round(time.time() * 1000)

    if not headers:
        # Contexto simulado para testes locais (Flask, curl, etc.)
        return {
            "awsRequestId": str(uuid.uuid4()),
            "functionName": os.getenv("AWS_LAMBDA_FUNCTION_NAME", "local-function"),
            "functionVersion": "$LATEST",
            "invokedFunctionArn": "arn:aws:lambda:local:0:function:local-function",
            "memoryLimitInMB": os.getenv("AWS_LAMBDA_FUNCTION_MEMORY_SIZE", "128"),
            "logGroupName": "/aws/lambda/local-function",
            "logStreamName": f"{time.strftime('%Y/%m/%d')}/[$LATEST]local",
            "getRemainingTimeInMillis": lambda: 30000
        }

    # Contexto real para quando executado via Lambda Runtime API
    deadline_ms = int(headers.get("lambda-runtime-deadline-ms", now_ms() + 15000))

    return {
        "awsRequestId": headers.get("lambda-runtime-aws-request-id", str(uuid.uuid4())),
        "functionName": os.getenv("AWS_LAMBDA_FUNCTION_NAME", "lambda-function"),
        "functionVersion": os.getenv("AWS_LAMBDA_FUNCTION_VERSION", "$LATEST"),
        "invokedFunctionArn": headers.get("lambda-runtime-invoked-function-arn", ""),
        "memoryLimitInMB": os.getenv("AWS_LAMBDA_FUNCTION_MEMORY_SIZE", "128"),
        "logGroupName": os.getenv("AWS_LAMBDA_LOG_GROUP_NAME", "/aws/lambda/lambda-function"),
        "logStreamName": os.getenv("AWS_LAMBDA_LOG_STREAM_NAME", f"{time.strftime('%Y/%m/%d')}/[$LATEST]auto"),
        "getRemainingTimeInMillis": lambda: max(deadline_ms - now_ms(), 0)
    }

