A basic slackbot.

# Environment Requirements
1) Python >= 3.10

# Slack Permission Requirements
## OAuth & Permissions > Scopes > Bot Token Scopes
1) channels:history
1) chat:write
1) reactions:read
1) users:read

## Event Subscriptions > Subscribe to bot events
1) message.channels
2) reaction_added

# Development
1) Follow the instructions
[here](https://slack.dev/bolt-python/tutorial/getting-started) to create and
install a new app and get your secret tokens.
1) `$ python3 -m venv .venv`
1) `$ source .venv/bin/activate`
1) `$ pip install -r requirements.txt`
1) `$ cp secrets-template.json secrets.json` and fill in your secrets
1) `$ npm install -g localtunnel` or locally if you want
1) `$ lt --port 3000 --subdomain yoursubdomainhere`
1) `$ python3 app.py`
1) Enable events at https://api.slack.com/apps/<your_workplace>/event-subscriptions?
1) Fill in the request URL as https://yoursubdomainhere.loca.lt/slack/events
1) Test & save changes
1) Your bot should now be able to respond to commands!
