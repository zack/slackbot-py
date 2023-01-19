import learn
import plus

class ReactionDispatcher:
    def __init__(self, app, context, body):

        self.app = app
        self.body = body
        self.context = context

        self.reaction = body['event']['reaction']

        self._dispatch()

    def _dispatch(self):
        match self.reaction:
            case "learn":
                self._call_with_app(learn.react_learn)
            case "unlearn":
                self._call_with_app(learn.react_unlearn)
            case "heavy_plus_sign":
                self._call_with_app(plus.react_plus)
            case "plus_one":
                self._call_with_app(plus.react_plus)

    def _call(self, func):
        func(self.body, self.context.say)

    def _call_with_app(self, func):
        func(self.body, self.context.say, self.app)
