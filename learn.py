from respond import respond_threaded

def learn(body, say):
    target_user = body['event']['item_user']
    source_user = body['event']['user']
    respond_threaded(say, body, f"Learned message to <@{target_user}> (by <@{source_user}>)")

def unlearn(body, say):
    target_user = body['event']['item_user']
    source_user = body['event']['user']
    respond_threaded(say, body, f"Unlearned message from <@{target_user}> (by <@{source_user}>)")
