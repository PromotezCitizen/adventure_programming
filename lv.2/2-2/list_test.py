import random
from collections import Counter

data = [ random.randint(1,4) for _ in range(30) ]

counter = Counter(data)
print(dict(counter))

print(data)
print('')
for x in data:
    while x in data:
        if x in data:
            data.remove(x)
    print(data, end="\n\n")
print(data)