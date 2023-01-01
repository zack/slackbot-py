from respond import respond

def spongecase(body, say, args):
    up = True
    out = ""

    for character in " ".join(args):
        if not character.isalpha():
            out += character
            continue

        if up:
            out += character.upper()
        else:
            out += character.lower()
        up = not up

    respond(say, body, out)
