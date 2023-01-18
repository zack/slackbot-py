import json
import os
import re

from slack_bolt import App

from command_dispatcher import CommandDispatcher
from reaction_dispatcher import ReactionDispatcher

def read_secrets():
    filename = os.path.join('secrets.json')
    try:
        with open(filename, mode='r') as f:
            return json.loads(f.read())
    except FileNotFoundError:
        return {}

secrets = read_secrets()

token=os.getenv('SLACK_CLIENT_SECRET') or secrets.get('SLACK_CLIENT_SECRET', '')
signing_secret=os.getenv('SLACK_SIGNING_SECRET') or secrets.get('SLACK_SIGNING_SECRET', '')

app = App(token=token, signing_secret=signing_secret)

# Messages that start with a question mark are bot commands
@app.message(re.compile("^\?(\S+)\s?(.*)$"))
def dispatch_command(context, body):
    CommandDispatcher(app, context, body)

@app.event("reaction_added")
def reaction_added(context, body):
    ReactionDispatcher(app, context, body)

# Start your app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
