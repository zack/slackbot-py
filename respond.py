# This will respond into a thread if the instigating message was already in a
# thread but otherwise will respond to the top level of the channel
def respond(say, body, out):
    is_threaded = body["event"].get("thread_ts", "") != ""

    if is_threaded:
        respond_threaded(say, body, out)
    else:
        respond_unthreaded(say, out)

# Will always respond into the top level of the channel of the instigating
# message, even if that message was in a thread.
def respond_unthreaded(say, out):
    say(out)

# Will always forcibly respond inside of a thread. If the instigating message
# was unthreaded this will start a thread off of that message. If the
# instigating message was threaded it will respond in the existing thread.
def respond_threaded(say, body, out):
    event = body["event"]

    thread_ts = (event.get("thread_ts", None)
        or event.get("ts", None)
        or event.get('item', {}).get('ts', None))
    say(out, thread_ts=thread_ts)

