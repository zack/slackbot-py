import sqlite3
from random import choice

from slack_sdk.errors import SlackApiError

from respond import respond, respond_threaded

def get_cursor():
    db = sqlite3.connect("learns.db", isolation_level=None) # autommit
    cur = db.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS learns(\
                learnee TEXT,\
                learner TEXT,\
                content TEXT,\
                ts DATETIME DEFAULT CURRENT_TIMESTAMP,\
                unique(learnee, content))"
    )
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

def learn(body, say, args, app):
    cur = get_cursor()

    if not user_exists(app, say, body, args[0]):
        return

    learner = body['event']['user']

    learnee = clean_user(args[0])
    if len(args) == 1:
        respond_threaded(say, body, "Can't learn an empty string!")
        return

    content = " ".join(args[1:])

    try:
        cur.execute("INSERT INTO learns(learnee, learner, content) values (?, ?, ?)", (learnee, learner, content))
    except sqlite3.IntegrityError:
        respond_threaded(say, body, f"I already know that one.")
        return

    respond_threaded(say, body, f"Learned to <@{learnee}>.")

def unlearn(body, say, args, app):
    cur = get_cursor()

    if not user_exists(app, say, body, args[0]):
        return

    learnee = clean_user(args[0])
    content = " ".join(args[1:])

    cur.execute("DELETE FROM learns where ? = learnee and ? = content", (learnee, content))

    if cur.rowcount == 0:
        out = "Sorry, nothing to unlearn."
    else:
        out = f"Unlearned message from <@{learnee}>)"

    respond_threaded(say, body, out)

def react_learn(body, say, app):
    cur = get_cursor()

    learnee = body['event']['item_user']
    learner = body['event']['user']

    message_ts = body['event']['item']['ts']
    channel = body['event']['item']['channel']

    content = app.client.conversations_history(
        channel=channel,
        inclusive=True,
        oldest=message_ts,
        limit=1
    )["messages"][0]["text"]

    try:
        cur.execute("INSERT INTO learns(learnee, learner, content) values (?, ?, ?)", (learnee, learner, content))
    except sqlite3.IntegrityError:
        respond_threaded(say, body, "I already know that one.")
        return

    respond_threaded(say, body, f"Learned message from <@{learnee}> (by <@{learner}>)")

def react_unlearn(body, say, app):
    cur = get_cursor()

    learnee = body['event']['item_user']
    learner = body['event']['user']

    message_ts = body['event']['item']['ts']
    channel = body['event']['item']['channel']

    content = app.client.conversations_history(
        channel=channel,
        inclusive=True,
        oldest=message_ts,
        limit=1
    )["messages"][0]["text"]

    cur.execute("DELETE FROM learns where ? = learnee and ? = content", (learnee, content))

    if cur.rowcount == 0:
        out = "Sorry, nothing to unlearn."
    else:
        out = f"Unlearned message from <@{learnee}> (by <@{learner}>)"

    respond_threaded(say, body, out)

def gimme(body, say, args, app):
    cur = get_cursor()

    if not user_exists(app, say, body, args[0]):
        return

    learnee = clean_user(args[0])

    cur.execute("SELECT content, ts FROM learns WHERE learnee = ?", [learnee])
    learns = cur.fetchall()
    learn = choice(learns)[0]
    ts = choice(learns)[1]

    out = f"<@{learnee}> on {ts}: {learn}"

    respond(say, body, out)
