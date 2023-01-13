import sqlite3
from respond import respond_threaded

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

def learn(body, say, app):
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
        respond_threaded(say, body, f"Already learned that message.")
        return

    respond_threaded(say, body, f"Learned message from <@{learnee}> (by <@{learner}>)")

def unlearn(body, say, app):
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
