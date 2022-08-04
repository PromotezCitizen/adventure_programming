class T():
    def __init__(self):
        self._a = "asdf"

    def print(self):
        return self._a


def test(cls):
    print(cls.print(), type(cls))

t = T()
print(type(t))
test(t)