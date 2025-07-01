import os
import uuid

def get_context():
    return {
        "aws_request_id": str(uuid.uuid4()),
        "function_name": os.getenv("AWS_LAMBDA_FUNCTION_NAME", "local-function"),
        "memory_limit_in_mb": os.getenv("AWS_LAMBDA_FUNCTION_MEMORY_SIZE", "128"),
        "remaining_time_in_millis": 30000,
    }

