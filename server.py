#!/bin/env python

import os
from http.server import *
from api import api_handler
from redirector import redirect_handler

APP_URL = "https://app.qwic.click"

class QwicClick(BaseHTTPRequestHandler):

    def redirect_to(self, location):
        self.send_response(301)
        self.send_header("Location", location)
        self.send_header("EndServer", "QwicClick Redirection Server/0.0.1")
        self.end_headers()
        self.wfile.write(bytes("Redirecting", "utf-8"))
    
    def return_invalid(self):
        self.send_response(400)
        self.send_header("EndServer", "QwicClick Redirection Server/0.0.1")
        self.end_headers()
        self.wfile.write(bytes("Invalid Shortlink", "utf-8"))

    def version_string(self):
        return "QwicClick Redirection Server/0.0.1"

    def do_GET(self):
        match self.path:
            case "/":
                self.redirect_to(APP_URL)
            case "/api":
                api_handler(self, self.path)
            case _:
                redirect_handler(self, self.path)

    def do_POST(self):
        match self.path:
            case "/":
                self.redirect_to(APP_URL)
            case "/api":
                api_handler(self, self.path)
            case _:
                redirect_handler(self, self.path)

def serve(PORT, ADDRESS):
    with HTTPServer((ADDRESS, PORT), QwicClick) as httpd:
        print(f"Serving on {ADDRESS}:{PORT}")
        httpd.serve_forever()