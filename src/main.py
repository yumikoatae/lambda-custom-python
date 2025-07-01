import sys
import json
from handlers.apigateway import handle_apigateway
from handlers.sqs import handle_sqs
from runtime.context import get_context
from runtime.libs.log import write

def handler(event, context):
    if "httpMethod" in event:
        return handle_apigateway(event, context)
    elif "Records" in event:
        return handle_sqs(event, context)
    else:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Unknown event"})
        }

def main():
    raw_input = sys.stdin.read()
    event = json.loads(raw_input)
    context = get_context()
    response = handler(event, context)
    print(json.dumps(response))

