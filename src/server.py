from flask import Flask, request, jsonify
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from main import handler
from runtime.context import get_context

app = Flask(__name__)

@app.route("/apigateway", methods=["GET", "POST"])
def simulate_apigateway():
    event = {
        "httpMethod": request.method,
        "path": request.path,
        "headers": dict(request.headers),
        "body": request.get_data(as_text=True)
    }
    context = get_context()
    response = handler(event, context)
    return jsonify(response)

@app.route("/sqs", methods=["POST"])
def simulate_sqs():
    # Espera um JSON com Records no estilo do SQS
    event = request.get_json(force=True)
    context = get_context()
    response = handler(event, context)
    return jsonify(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9001)

