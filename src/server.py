import json
from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException

class WebApp:
    def __init__(self):
        self.url_map = Map([
            Rule("/apigateway", endpoint="apigateway", methods=["GET", "POST"]),
            Rule("/sqs", endpoint="sqs", methods=["POST"]),
        ])

    def on_apigateway(self, request):
        """
        Simula uma chamada do API Gateway diretamente para o handler do apigateway.
        """
        from handlers import apigateway
        from runtime.context import create_context

        event = {
            "httpMethod": request.method,
            "path": request.path,
            "headers": dict(request.headers),
            "body": request.get_data(as_text=True)
        }
        context = create_context()
        result = apigateway.handler(event, context)

        return Response(json.dumps(result), mimetype='application/json')

    def on_sqs(self, request):
        """
        Simula uma chamada do SQS diretamente para o handler do sqs.
        """
        from handlers import sqs
        from runtime.context import create_context

        event = json.loads(request.get_data())
        context = create_context()
        result = sqs.handler(event, context)

        return Response(json.dumps(result), mimetype='application/json')

    def dispatch_request(self, request):
        adapter = self.url_map.bind_to_environ(request.environ)
        try:
            endpoint, values = adapter.match()
            handler = getattr(self, f'on_{endpoint}')
            return handler(request, **values)
        except HTTPException as e:
            return e

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)

server = WebApp()

if __name__ == "__main__":
    from werkzeug.serving import run_simple
    run_simple("0.0.0.0", 9001, server)
