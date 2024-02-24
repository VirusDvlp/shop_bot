


class Or:


    def __init__(self, *filters):
        self.filters = filters


    def __call__(self, message):
        for f in self.filters:
            if f(message):
                return True
