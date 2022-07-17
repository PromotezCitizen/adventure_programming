import random
import numpy as np
from pynput import keyboard

puzzle_size = 3
puzzle = [ x for x in range(puzzle_size**2)]
puzzle = np.reshape(np.array(puzzle), (3, 3))

x_pos, y_pos = 0, 0 # x_pos : row, y_pos : column
shake_forward = []

# puzzle init
for i in range(100):
    mv = random.randint(0, 3)

    if mv == 0: # up
        try:
            x_pos -= 1
            if x_pos < 0: raise
            shake_forward.append(mv)
            temp = puzzle[x_pos+1][y_pos]
            puzzle[x_pos+1][y_pos] = puzzle[x_pos][y_pos]
            puzzle[x_pos][y_pos] = temp
            print(mv, puzzle, end="\n\n")
        except:
            x_pos += 1

    if mv == 1: # left
        try:
            y_pos -= 1
            if y_pos < 0 : raise
            shake_forward.append(mv)
            temp = puzzle[x_pos][y_pos+1]
            puzzle[x_pos][y_pos+1] = puzzle[x_pos][y_pos]
            puzzle[x_pos][y_pos] = temp
            print(mv, puzzle, end="\n\n")
        except:
            y_pos += 1

    if mv == 2: # right
        try:
            y_pos += 1
            if y_pos >= puzzle_size: raise
            shake_forward.append(mv)
            temp = puzzle[x_pos][y_pos-1]
            puzzle[x_pos][y_pos-1] = puzzle[x_pos][y_pos]
            puzzle[x_pos][y_pos] = temp
            print(mv, puzzle, end="\n\n")
        except:
            y_pos -= 1

    if mv == 3: # down
        try:
            x_pos += 1
            if x_pos >= puzzle_size: raise
            shake_forward.append(mv)
            temp = puzzle[x_pos-1][y_pos]
            puzzle[x_pos-1][y_pos] = puzzle[x_pos][y_pos]
            puzzle[x_pos][y_pos] = temp
            print(mv, puzzle, end="\n\n")
        except:
            x_pos -= 1

# 3 - mv == offsite movement

def printForward(arr):
    print("[", end="")
    for data in arr:
        if data == 0:
            data = "u"
        if data == 1:
            data = "l"
        if data == 2:
            data = "r"
        if data == 3:
            data = "d"
        print(data, end=",")
    print("]")


# movement optimize
x_f = False
for _ in range(100):
    printForward(shake_forward)
    for idx, data in enumerate(shake_forward[:-1]):
        if (3 - shake_forward[idx+1] == data):
            shake_forward.pop(idx+1)
            shake_forward.pop(idx)
            x_f = False
            break
        x_f = True
    if x_f:
        break

def mv_up():
    global x_pos, y_pos, puzzle, shake_forward
    try:
        x_pos -= 1
        if x_pos < 0: raise
        if 3 - shake_forward[-1] == 0:
            shake_forward.pop(-1)
        else:
            shake_forward.push(0)
        temp = puzzle[x_pos+1][y_pos]
        puzzle[x_pos+1][y_pos] = puzzle[x_pos][y_pos]
        puzzle[x_pos][y_pos] = temp
        print(mv, puzzle, end="\n\n")
    except:
        x_pos += 1

def mv_down():
    global x_pos, y_pos, puzzle, shake_forward
    try:
        x_pos -= 1
        if x_pos < 0: raise
        if 3 - shake_forward[-1] == 3:
            shake_forward.pop(-1)
        else:
            shake_forward.push(3)
        temp = puzzle[x_pos+1][y_pos]
        puzzle[x_pos+1][y_pos] = puzzle[x_pos][y_pos]
        puzzle[x_pos][y_pos] = temp
        print(mv, puzzle, end="\n\n")
    except:
        x_pos += 1

def mv_left():
    global x_pos, y_pos, puzzle, shake_forward
    try:
        x_pos -= 1
        if x_pos < 0: raise
        if 3 - shake_forward[-1] == 1:
            shake_forward.pop(-1)
        else:
            shake_forward.push(1)
        temp = puzzle[x_pos+1][y_pos]
        puzzle[x_pos+1][y_pos] = puzzle[x_pos][y_pos]
        puzzle[x_pos][y_pos] = temp
        print(mv, puzzle, end="\n\n")
    except:
        x_pos += 1

def mv_right():
    global x_pos, y_pos, puzzle, shake_forward
    try:
        y_pos += 1
        if y_pos >= puzzle_size: raise
        if 3 - shake_forward[-1] == 2:
            shake_forward.pop(-1)
        else:
            shake_forward.push(2)
        temp = puzzle[x_pos+1][y_pos]
        puzzle[x_pos+1][y_pos] = puzzle[x_pos][y_pos]
        puzzle[x_pos][y_pos] = temp
        print(mv, puzzle, end="\n\n")
    except:
        y_pos -= 1

def on_release(key):
    print(key)
    if key == keyboard.Key.up:
        mv_up()
    if key == keyboard.Key.down:
        mv_down()
    if key == keyboard.Key.left:
        mv_left()
    if key == keyboard.Key.right:
        mv_right()

    if key == keyboard.Key.esc:
        return False



with keyboard.Listener(on_release=on_release) as listener:
    listener.join()