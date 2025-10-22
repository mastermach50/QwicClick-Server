import json
import database as db
import canned_responses as cr
from http.server import BaseHTTPRequestHandler

from security import with_session

def api_handler(handler, path):
    match path[1]:
        case "ping": ping(handler)
        case "login": login(handler)
        case "register": register(handler)
        case "add_link": add_link(handler)
        case "update_link": update_link(handler)
        case "delete_link": delete_link(handler)
        case "get_all_links": get_all_links(handler)
        case "get_link_stats": get_link_stats(handler)
        case "whoami": whoami(handler)
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

def ping(handler):
    cr.send_text(handler, 200, f"pong from {handler.version_string()}")


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
            if sessiontoken is None:
                cr.server_error(handler)
                return

            cr.send_json(handler, 200, {'sessiontoken': sessiontoken})

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
            cr.send_json(handler, 200, {'userid': userid})

@with_session
def add_link(handler, userid):
    post_data = get_data(handler)
    if post_data is None:
        return

    data = db.add_link(userid, post_data.get("shortlink"), post_data.get("longlink"))

    match data:
        case "shortlink already exists":
            cr.bad_request(handler, "Shortlink already exists")
        case None:
            cr.server_error(handler)
        case _:
            (linkid, shortlink, longlink) = data
            cr.send_json(handler, 200, {"linkid": linkid, "shortlink": shortlink, "longlink": longlink})

@with_session
def update_link(handler, userid):
    post_data = get_data(handler)
    if post_data is None:
        return

    result = db.update_link(post_data.get("linkid"), post_data.get("shortlink"), post_data.get("longlink"))

    match result:
        case True:
            cr.send_text(handler, 200, "Link updated")
        case False:
            cr.server_error(handler)

@with_session
def delete_link(handler, userid):
    post_data = get_data(handler)
    if post_data is None:
        return

    result = db.delete_link(post_data.get("linkid"))

    match result:
        case True:
            cr.send_text(handler, 200, "Link deleted")
        case False:
            cr.server_error(handler)


@with_session
def get_all_links(handler, userid):
    links = db.get_all_links(userid)

    match links:
        case None:
            cr.server_error(handler)
        case _:
            cr.send_json(handler, 200, {"links": links})

@with_session
def get_link_stats(handler, userid):
    post_data = get_data(handler)
    if post_data is None:
        return
    
    linkid = post_data.get("linkid")
    count = db.get_link_stats(linkid)

    match count:
        case "link does not exist":
            cr.not_found(handler, "Link does not exist")
        case None:
            cr.server_error(handler)
        case _:
            cr.send_json(handler, 200, {"count": count})

@with_session
def whoami(handler, userid):
    data = db.get_user_info(userid)
    cr.send_json(handler, 200, {"username": data[0], "email": data[1]})