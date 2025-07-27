from http.server import *

PORT = 3310

class QwicClick(BaseHTTPRequestHandler):

    def redirect_to_app(self):
        self.send_response(301)
        self.send_header("Location", "https://app.qwic.click")
        self.end_headers()
        self.wfile.write(bytes("Redirecting", "utf-8"))

    def version_string(self):
        return "QwicClick Redirection Server/0.0.1"

    def do_GET(self):
        self.redirect_to_app()

with HTTPServer(('', PORT), QwicClick) as httpd:
    print("Serving on " + str(PORT))
    httpd.serve_forever()