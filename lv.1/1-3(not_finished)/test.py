import random

def checkPossibilityNMove(mv, beetle_pos, map_size):
    if mv == 0:
        if beetle_pos['row'] == 0:
            return False
        beetle_pos['row'] -= 1
        return True
    if mv == 1:
        if beetle_pos['col'] == 0:
            return False
        beetle_pos['col'] -= 1
        return True
    if mv == 2:
        if beetle_pos['row'] == map_size - 1:
            return False
        beetle_pos['row'] += 1
        return True
    if mv == 3:
        if beetle_pos['col'] == map_size - 1:
            return False
        beetle_pos['col'] += 1
        return True

map_size = 6
num_roach = 3

beetle_pos = [ {
        'row':random.randint(0, map_size-1),
        'col':random.randint(0, map_size-1)
    } for _ in range(num_roach) ]

print(beetle_pos)


for position in beetle_pos:
    print(checkPossibilityNMove(random.randint(0, 3), position, map_size))

print(beetle_pos)