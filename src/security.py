from http.server import BaseHTTPRequestHandler
import canned_responses as cr
import database as db

def with_session(func):
    def wrapper(handler: BaseHTTPRequestHandler):
        sessiontoken = handler.headers.get('sessiontoken')
        if sessiontoken is None:
            cr.unauthorized(handler, "Missing sessiontoken header")
            return

        userid = db.verify_session(sessiontoken)
        if userid == "session does not exist":
            cr.unauthorized(handler, "Invalid sessiontoken")
            return
        elif userid is None:
            cr.server_error(handler)
            return

        result = func(handler, userid)
        return result
    return wrapper