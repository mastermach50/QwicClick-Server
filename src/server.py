#!/bin/env python

import os
from http.server import *
from api import api_handler
from redirector import redirect_handler
import canned_responses as cr

APP_URL = "https://app.qwic.click"

class QwicClick(BaseHTTPRequestHandler):

    def end_headers(self):
        self.send_header("EndServer", "QwicClick Redirection Server/0.0.1")
        return super().end_headers()

    def version_string(self):
        return "QwicClick Redirection Server/0.0.1"

    def do_GET(self):
        self.qwicclick_handle_request()

    def do_POST(self):
        self.qwicclick_handle_request()

    def qwicclick_handle_request(self):
        path = self.path.strip("/").split("/")

        match path[0]:
            case "":
                cr.redirect_to(self, APP_URL)
            case "api":
                api_handler(self, path)
            case _:
                redirect_handler(self, path)

def serve(PORT, ADDRESS):
    with HTTPServer((ADDRESS, PORT), QwicClick) as httpd:
        print(f"Serving on {ADDRESS}:{PORT}")
        httpd.serve_forever()