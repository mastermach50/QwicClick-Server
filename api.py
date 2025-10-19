def api_handler(handler, path):
    handler.send_response(200)
    handler.wfile.write(bytes("API to be implemented", "utf-8"))