import random

class C():
    def __init__(self):
        self.arr = []
        for idx in range(10):
            temp = [idx, random.randrange(1, 10)]
            self.arr.append(temp)

    def test(self):
        print(self.arr)
        for data in self.arr:
            data[1] += 1
        print(self.arr)

C().test()