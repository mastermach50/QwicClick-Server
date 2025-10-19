
short2long = {
    "/design": "https://www.figma.com/design/cP4r2oxky5hL0G0ThpUuGB/QwicClick?node-id=0-1&t=sYT4aplf9E7S5wTc-1"
}

def redirect_handler(handler, path):
    if short2long.get(path) != None:
        print(f"Redirect {short2long[path]}")
        handler.redirect_to(short2long[path])
    else:
        print(f"Invalid shortlink {path}")
        handler.return_invalid()
