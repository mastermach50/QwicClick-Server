import json


def redirect_to(handler, url):
    handler.send_response(301)
    handler.send_header("Location", url)
    handler.end_headers()
    handler.wfile.write(bytes("Redirecting...", "utf-8"))

def bad_request(handler, message="Bad request"):
    handler.send_response(400)
    handler.end_headers()
    handler.wfile.write(bytes(message, "utf-8"))

def unauthorized(handler, message="Unauthorized"):
    handler.send_response(401)
    handler.end_headers()
    handler.wfile.write(bytes(message, "utf-8"))

def not_found(handler, message="Not found"):
    handler.send_response(404)
    handler.end_headers()
    handler.wfile.write(bytes(message, "utf-8"))

def server_error(handler):
    handler.send_response(500)
    handler.end_headers()
    handler.wfile.write(bytes("Internal server error", "utf-8"))

def send_json(handler, code, data):
    handler.send_response(code)
    handler.send_header('Content-Type', 'application/json')
    handler.end_headers()
    handler.wfile.write(
        json.dumps(data).encode('utf-8')
    )

def send_text(handler, code, data):
    handler.send_response(code)
    handler.send_header('Content-Type', 'text/plain')
    handler.end_headers()
    handler.wfile.write(bytes(data, "utf-8"))