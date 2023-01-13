import bubble
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
        match self.command:
            case "bubble":
                self._call(bubble.white)
            case "bubble-y":
                self._call(bubble.yellow)
            case "bubble-a":
                self._call(bubble.alternate)
            case "bubble-r":
                self._call(bubble.rand)
            case "spongecase":
                self._call(spongecase.spongecase)
            case "plus":
                self._call_with_app(plus.plus)
            case "pluses":
                self._call_with_app(plus.pluses)

    def _call(self, func):
        func(self.body, self.context.say, self.args)

    def _call_with_app(self, func):
        func(self.body, self.context.say, self.args, self.app)
