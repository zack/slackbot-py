import bubble
import spongecase

class CommandDispatcher:
    def __init__(self, context, body):

        self.context = context
        self.body = body

        self.args = context.matches[1].split(" ")
        self.command = context.matches[0]

        self.dispatch()

    def dispatch(self):
        match self.command:
            case "bubble":
                bubble.white(self.body, self.context.say, self.args)
            case "bubble-y":
                bubble.yellow(self.body, self.context.say, self.args)
            case "bubble-a":
                bubble.alternate(self.body, self.context.say, self.args)
            case "bubble-r":
                bubble.rand(self.body, self.context.say, self.args)
            case "spongecase":
                spongecase.spongecase(self.body, self.context.say, self.args)
