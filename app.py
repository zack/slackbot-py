import json
import os
import re

from slack_bolt import App

from command_dispatcher import CommandDispatcher

def read_secrets():
    filename = os.path.join('secrets.json')
    try:
        with open(filename, mode='r') as f:
            return json.loads(f.read())
    except FileNotFoundError:
        return {}

secrets = read_secrets()

app = App(
    token=secrets['SLACK_TOKEN'],
    signing_secret=secrets['SLACK_SIGNING_SECRET']
)

# Messages that start with a question mark are bot commands
@app.message(re.compile("^\?(\S+)\s(.*)$"))
def dispatch_command(context, body):
    CommandDispatcher(context, body)

# Start your app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
