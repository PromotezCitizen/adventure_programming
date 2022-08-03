operators = {
    'add': '+',
    'sub': '-',
    'mult': '*',
    'div': '/',
    'mod': '%',
    'gt': '<',
    'lt': '>',
    'ge': '<=',
    'le': '>=',
    'eq': '==',
    'ne': '!=',
    'and': 'and',
    'or': 'or'
}

num1 = 2
num2 = 5

for op in operators.values():
    print(eval('{0} {1} {2}'.format(num1, op, num2)))

arr = [ 3, 6, 9 ]

t = arr[1]
t = 4

class t2():
    def __init__(self, arr):
        self.arr = arr
    
    def change(self):
        self.arr[3] = 100

    def print(self):
        print(self.arr)

class t1():
    def __init__(self):
        self.arr = [ x for x in range(5)]
        self.test = t2(self.arr)
        self.__asdf = 10

    def run(self):
        self.print()
        self.test.change()
        self.test.print()
        self.print()

    def print(self):
        print(self.arr)

test = t1()
test.run()