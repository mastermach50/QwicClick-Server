import canned_responses as cr

short2long = {
    "design": "https://www.figma.com/design/cP4r2oxky5hL0G0ThpUuGB/QwicClick?node-id=0-1&t=sYT4aplf9E7S5wTc-1"
}

def redirect_handler(handler, path):
    longlink = short2long.get(path[0])
    if longlink is not None:
        print(f"Redirect to {longlink}")
        cr.redirect_to(handler, longlink)
    else:
        print(f"Invalid shortlink {path[0]}")
        cr.invalid(handler)
