import bubble
import learn
import ping
import plus
import spongecase

class CommandDispatcher:
    def __init__(self, app, context, body):

        self.app = app
        self.body = body
        self.context = context

        self.args = context.matches[1].split(" ")
        self.command = context.matches[0]

        self._dispatch()

    def _dispatch(self):
        print(self.command)
        match self.command:
            case "bubble":
                self._call(bubble.white)
            case "bubble-y":
                self._call(bubble.yellow)
            case "bubble-a":
                self._call(bubble.alternate)
            case "bubble-r":
                self._call(bubble.rand)
            case "gimme":
                self._call_with_app(learn.gimme)
            case "learn":
                self._call_with_app(learn.learn)
            case "ping":
                self._call(ping.pong)
            case "plus":
                self._call_with_app(plus.plus)
            case "pluses":
                self._call_with_app(plus.pluses)
            case "spongecase":
                self._call(spongecase.spongecase)
            case "unlearn":
                self._call_with_app(learn.unlearn)
            case "++":
                self._call_with_app(plus.plus)

    def _call(self, func):
        func(self.body, self.context.say, self.args)

    def _call_with_app(self, func):
        func(self.body, self.context.say, self.args, self.app)
