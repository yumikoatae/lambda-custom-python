def handle_apigateway(event, context):
    return {
        "statusCode": 200,
        "body": f"✅ API Gateway recebeu: {event.get('path', '/')}"
    }

