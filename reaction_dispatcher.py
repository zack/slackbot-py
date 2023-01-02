import learn

class ReactionDispatcher:
    def __init__(self, context, body):

        self.context = context
        self.body = body

        self.reaction = body['event']['reaction']

        self.dispatch()

    def dispatch(self):
        match self.reaction:
            case "learn":
                learn.learn(self.body, self.context.say)
            case "unlearn":
                learn.unlearn(self.body, self.context.say)
