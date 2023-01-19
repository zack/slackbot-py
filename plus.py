import random
import re
import sqlite3

from slack_sdk.errors import SlackApiError

from respond import respond, respond_threaded

def get_cursor():
    db = sqlite3.connect("pluses.db", isolation_level=None) # autommit
    cur = db.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS pluses(plusee TEXT, pluser TEXT, note TEXT, ts DATETIME DEFAULT CURRENT_TIMESTAMP)")
    return cur

def user_exists(app, say, body, user):
    try:
        app.client.users_info(user=clean_user(user))
        return True
    except SlackApiError as e:
        respond_threaded(say, body, f"Sorry, I don't know who {user} is.")
        return False

def clean_user(user):
    return user[2:-1] # strip <@ and >

def plus(body, say, args, app):
    cur = get_cursor()

    if not user_exists(app, say, body, args[0]):
        return

    plusee = clean_user(args[0])
    pluser = body['event']['user']
    pluser_name = app.client.users_info(user=pluser)['user']['profile']['display_name']

    if len(args) == 1:
        note = ""
    elif args[1].lower() == 'for':
        # strip out 'for'
        note = " ".join(args[2:])
    else:
        note = " ".join(args[1:])


    if plusee == pluser:
        out = "Hey, no plussing yourself! :)"
        return

    cur.execute("INSERT INTO pluses(plusee, pluser, note) values (?, ?, ?)", (plusee, pluser, note))
    cur.execute("SELECT count(*) FROM pluses WHERE plusee = ?", [plusee])
    plusee_plus_count = cur.fetchone()[0]
    for_note = ''
    if note:
        for_note = f" for *\"{note}\"*"
    out = f"{pluser_name} has plussed <@{plusee}>{for_note}! <@{plusee}> now has *{plusee_plus_count} pluses*!"

    respond_threaded(say, body, out)

def react_plus(body, say):
    cur = get_cursor()

    plusee = body['event']['item_user']
    pluser = body['event']['user']
    pluser_name = app.client.users_info(user=pluser)['user']['profile']['display_name']

    if plusee == pluser:
        out = "Hey, no plussing yourself! :)"
        return

    cur.execute("INSERT INTO pluses(plusee, pluser) values (?, ?)", (plusee, pluser))
    cur.execute("SELECT count(*) FROM pluses WHERE plusee = ?", [plusee])
    plusee_plus_count = cur.fetchone()[0]
    out = f"{pluser_name} has plussed <@{plusee}>! <@{plusee}> now has *{plusee_plus_count} pluses*!"

    respond_threaded(say, body, out)

def pluses(body, say, args, app):
    cur = get_cursor()

    if not user_exists(app, say, body, args[0]):
        return

    user = clean_user(args[0])
    asker = body['event']['user']

    cur.execute("SELECT count(*) FROM pluses WHERE plusee = ?", [user])

    user_plus_count = cur.fetchone()[0]

    if user == asker:
        out = f"You have *{user_plus_count} pluses*!"
    else:
        out = f"<@{user}> has *{user_plus_count} pluses*!"

    respond(say, body, out)
