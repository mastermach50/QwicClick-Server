#!/bin/env python

from http.server import *

PORT = 3300
ADDRESS = "0.0.0.0"

class QwicClick(BaseHTTPRequestHandler):

    def redirect_to(self, location):
        self.send_response(301)
        self.send_header("Location", location)
        self.send_header("EndServer", "QwicClick Redirection Server/0.0.1")
        self.end_headers()
        self.wfile.write(bytes("Redirecting", "utf-8"))

    def version_string(self):
        return "QwicClick Redirection Server/0.0.1"

    def do_GET(self):
        if (self.path == "/design"):
            self.redirect_to("https://www.figma.com/design/cP4r2oxky5hL0G0ThpUuGB/QwicClick?node-id=0-1&t=sYT4aplf9E7S5wTc-1")
        else:
            self.redirect_to("https://app.qwic.click")

with HTTPServer((ADDRESS, PORT), QwicClick) as httpd:
    print(f"Serving on {ADDRESS}:{PORT}")
    httpd.serve_forever()
