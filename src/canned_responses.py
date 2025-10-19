def invalid(handler):
    handler.send_response(400)
    handler.end_headers()
    handler.wfile.write(bytes("Invalid request", "utf-8"))

def not_found(handler):
    handler.send_response(404)
    handler.end_headers()
    handler.wfile.write(bytes("Not found", "utf-8"))

def server_error(handler):
    handler.send_response(500)
    handler.end_headers()
    handler.wfile.write(bytes("Server error", "utf-8"))

def redirect_to(handler, url):
    handler.send_response(301)
    handler.send_header("Location", url)
    handler.end_headers()
    handler.wfile.write(bytes("Redirecting...", "utf-8"))