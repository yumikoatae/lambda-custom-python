import json
from server import server
from werkzeug.test import EnvironBuilder
from werkzeug.wrappers import Request

def handler(event, context):
    if "httpMethod" in event:
        builder = EnvironBuilder(
            path=event.get("path", "/apigateway"),
            method=event["httpMethod"],
            headers=event.get("headers"),
            data=event.get("body", ""),
        )
        env = builder.get_environ()
        request = Request(env)
        response = server.dispatch_request(request)
        return {
            "statusCode": response.status_code,
            "headers": dict(response.headers),
            "body": response.get_data(as_text=True),
        }

    elif "Records" in event:
        builder = EnvironBuilder(
            path="/sqs",
            method="POST",
            data=json.dumps(event),
            headers={"Content-Type": "application/json"},
        )
        env = builder.get_environ()
        request = Request(env)
        response = server.dispatch_request(request)
        return {
            "statusCode": response.status_code,
            "headers": dict(response.headers),
            "body": response.get_data(as_text=True),
        }

    return {
        "statusCode": 400,
        "body": json.dumps({"error": "Unsupported event type"}),
    }
