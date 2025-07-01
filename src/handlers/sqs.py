def handle_sqs(event, context):
    records = event.get("Records", [])
    return {
        "statusCode": 200,
        "body": f"📬 Processados {len(records)} registros do SQS"
    }

