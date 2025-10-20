import json
import database as db
import canned_responses as cr
from http.server import BaseHTTPRequestHandler

def api_handler(handler, path):
    match path[1]:
        case "login": login(handler)
        case "register": register(handler)
        case _: cr.bad_request(handler)

def get_data(handler: BaseHTTPRequestHandler):
    content_length = int(handler.headers.get('Content-Length', 0))
    if content_length == 0:
        cr.bad_request(handler, "Empty request body or invalid Content-Length header")
        return None

    post_body_bytes = handler.rfile.read(content_length)

    try:
        post_data = json.loads(post_body_bytes)
        return post_data
    except:
        cr.bad_request(handler, "Invalid JSON in request body")
        return None


def login(handler):
    post_data = get_data(handler)
    if post_data is None:
        return

    userid = db.verify_user(post_data.get("email"), post_data.get("password"))

    match userid:
        case "user does not exist":
            cr.not_found(handler, "User does not exist")
        case "incorrect password":
            cr.unauthorized(handler, "Incorrect password")
        case None:
            cr.server_error(handler)
        case _:
            sessiontoken = db.create_session(userid)
            handler.send_response(200)
            handler.send_header('Content-Type', 'application/json')
            handler.end_headers()
            handler.wfile.write(
                json.dumps({'sessiontoken': sessiontoken}).encode('utf-8')
            )

def register(handler):
    post_data = get_data(handler)
    if post_data is None:
        return

    userid = db.add_user(post_data.get("email"), post_data.get("password"), post_data.get("username"))

    match userid:
        case "user exists":
            cr.bad_request(handler, "User already exists")
        case None:
            cr.server_error(handler)
        case _:
            handler.send_response(200)
            handler.send_header('Content-Type', 'application/json')
            handler.end_headers()
            handler.wfile.write(
                json.dumps({'userid': userid}).encode('utf-8')
            )
