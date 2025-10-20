import canned_responses as cr
import database as db

def redirect_handler(handler, path):
    longlink = db.get_longlink(path[0])

    if longlink is not None:
        print(f"Redirect to {longlink}")
        cr.redirect_to(handler, longlink)
    else:
        print(f"Invalid shortlink {path[0]}")
        cr.bad_request(handler, "Invalid shortlink")
