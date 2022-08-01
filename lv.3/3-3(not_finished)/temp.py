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