import learn
import plus

class ReactionDispatcher:
    def __init__(self, context, body):

        self.body = body
        self.context = context

        self.reaction = body['event']['reaction']

        self._dispatch()

    def _dispatch(self):
        match self.reaction:
            case "learn":
                self._call(learn.learn)
            case "unlearn":
                self._call(learn.unlearn)
            case "heavy_plus_sign":
                self._call(plus.react_plus)
            case "plus_one":
                self._call(plus.react_plus)

    def _call(self, func):
        func(self.body, self.context.say)
