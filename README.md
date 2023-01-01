A basic slackbot.

# Development
1) Follow the instructions
[here](https://slack.dev/bolt-python/tutorial/getting-started) to create and
install a new app and get your secret tokens.
1) `$ cp secrets-template.json secrets.json` and fill in your secrets
1) `$ npm install -g localtunnel` or locally if you want
1) `$ lt --port 3000 --subdomain yoursubdomainhere`
1) `$ python3 app.py`
1) Enable events at https://api.slack.com/apps/\<your_workplace\>/event-subscriptions?
1) Fill in the request URL as https://yoursubdomainhere.loca.lt/slack/events
1) Test & save changes
1) Your bot should now be able to respond to commands!