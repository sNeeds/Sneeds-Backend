class BooleanList(list):
    def __init__(self):
        super().__init__()

    def __bool__(self):
        return self[0]

    def __and__(self, other):
        return self[0] and other
