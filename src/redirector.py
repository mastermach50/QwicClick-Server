import canned_responses as cr
import database as db

def redirect_handler(handler, path):
    result = db.get_longlink(path[0])

    if result is not None:
        (linkid, longlink) = result
        print(f"Redirect to {longlink}")
        db.increment_count(linkid)
        cr.redirect_to(handler, longlink)
    else:
        print(f"Invalid shortlink {path[0]}")
        cr.bad_request(handler, "Invalid shortlink")
