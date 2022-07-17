import random
import numpy as np
from pynput import keyboard

class NPuzzle():
    def __init__(self):
        self.__puzzle_size = 3
        self.__puzzle = [ x for x in range(self.__puzzle_size**2)]
        self.__puzzle = np.reshape(np.array(self.__puzzle), (3, 3))
        self.__shake_forward = []
        self.__x_pos = 0
        self.__y_pos = 0
        self.__puzzle_init()
        self.__optimize_com_movement()
        self.__hint = 4
        self.__max_hint = self.__hint
    
    def __change_position(self, origin, to, show_flag=True): # __change_postion(origin: [x_pos,y_pos], to: [x_pos,y_pos])
        temp = self.__puzzle[origin[0]][origin[1]]
        self.__puzzle[origin[0]][origin[1]] = self.__puzzle[to[0]][to[1]]
        self.__puzzle[to[0]][to[1]] = temp
        if show_flag: print(self.__puzzle, end="\n\n")

    def __puzzle_init(self):
        for _ in range(100):
            mv = random.randint(0, 3)

            if mv == 0: # up
                try:
                    self.__x_pos -= 1
                    if self.__x_pos < 0: raise
                    self.__shake_forward.append(mv)
                    self.__change_position([self.__x_pos+1, self.__y_pos], [self.__x_pos, self.__y_pos], False)
                except:
                    self.__x_pos += 1

            if mv == 1: # left
                try:
                    self.__y_pos -= 1
                    if self.__y_pos < 0 : raise
                    self.__shake_forward.append(mv)
                    self.__change_position([self.__x_pos, self.__y_pos+1], [self.__x_pos, self.__y_pos], False)
                except:
                    self.__y_pos += 1

            if mv == 2: # right
                try:
                    self.__y_pos += 1
                    if self.__y_pos >= self.__puzzle_size: raise
                    self.__shake_forward.append(mv)
                    self.__change_position([self.__x_pos, self.__y_pos-1], [self.__x_pos, self.__y_pos], False)
                except:
                    self.__y_pos -= 1

            if mv == 3: # down
                try:
                    self.__x_pos += 1
                    if self.__x_pos >= self.__puzzle_size: raise
                    self.__shake_forward.append(mv)
                    self.__change_position([self.__x_pos-1, self.__y_pos], [self.__x_pos, self.__y_pos], False)
                except:
                    self.__x_pos -= 1

    def __optimize_com_movement(self):
        x_f = False
        for _ in range(100):
            #self.__print_forward()
            for idx, data in enumerate(self.__shake_forward[:-1]):
                if (3 - self.__shake_forward[idx+1] == data):
                    self.__shake_forward.pop(idx+1)
                    self.__shake_forward.pop(idx)
                    x_f = False
                    break
                x_f = True
            if x_f:
                break

    def __print_forward(self):
        print("[", end="")
        for data in self.__shake_forward:
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

    def __print_puzzle(self):
        None

    def print_puzzle(self):
        print(self.__puzzle)

    def mv_start(self):
        self.__shake_forward.reverse()
        print(self.__puzzle, end="\n\n")

    def mv_end(self):
        if len(self.__shake_forward) == 0:
            return True
        temp = [ x for x in range(self.__puzzle_size**2) ]
        temp = np.resize(np.array(temp), (3,3))
        if np.array_equal(temp, self.__puzzle):
            return True
        return False

    def mv_up(self):
        try:
            self.__x_pos -= 1
            if self.__x_pos < 0: raise
            self.__mv_forward_push(0)
            self.__change_position([self.__x_pos+1, self.__y_pos], [self.__x_pos, self.__y_pos])
        except:
            self.__x_pos += 1

        return self.mv_end()

    def mv_down(self):
        try:
            self.__x_pos += 1
            if self.__x_pos >= self.__puzzle_size: raise
            self.__mv_forward_push(3)
            self.__change_position([self.__x_pos-1, self.__y_pos], [self.__x_pos, self.__y_pos])
        except:
            self.__x_pos -= 1

        return self.mv_end()

    def mv_left(self):
        try:
            self.__y_pos -= 1
            if self.__y_pos < 0: raise
            self.__mv_forward_push(1)
            self.__change_position([self.__x_pos, self.__y_pos+1], [self.__x_pos, self.__y_pos])
        except:
            self.__y_pos += 1

        return self.mv_end()

    def mv_right(self):
        try:
            self.__y_pos += 1
            if self.__y_pos >= self.__puzzle_size: raise
            self.__mv_forward_push(2)
            self.__change_position([self.__x_pos, self.__y_pos-1], [self.__x_pos, self.__y_pos])
        except:
            self.__y_pos -= 1

        return self.mv_end()
        
    def __mv_forward_push(self, dir):
        if 3 - self.__shake_forward[0] == dir:
            self.__shake_forward.pop(0)
        else:
            self.__shake_forward.insert(0, dir)

    def auto_move(self):
        for _ in range(20):
            mv = self.__shake_forward[0]
            print('move to ', 3-mv, "|", self.__shake_forward)
            if mv == 0: # shaked to up -> restore: down
                self.mv_down()
            elif mv == 1: # shaked to left -> restore: right
                self.mv_right()
            elif mv == 2: # shaked to right -> restore: left
                self.mv_left()
            elif mv == 3: # shaked to up -> restore: up
                self.mv_up()

    def hint(self):
        if self.__hint < 1:
            return 'Not available hint: you have zero hint coin'
        data = 3 - self.__shake_forward[0]
        self.__hint -= 1
        msg = " - hint coin left (%d/%d)" % (self.__hint, self.__max_hint)
        if data == 0:
            return "UP" + msg
        if data == 1:
            return "LEFT" + msg
        if data == 2:
            return "RIGHT" + msg
        if data == 3:
            return "DOWN" + msg

def on_press(key):
    end = True
    try:
        if key.char == 'h':
            print(test.hint())
    except:
        None
    if key == keyboard.Key.up:
        end = test.mv_up()
    elif key == keyboard.Key.down:
        end = test.mv_down()
    elif key == keyboard.Key.left:
        end = test.mv_left()
    elif key == keyboard.Key.right:
        end = test.mv_right()
    if end == True:
        return False
    if key == keyboard.Key.esc:
        return False

while True:
    print("start")
    test = NPuzzle()
    test.mv_start()
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
    print("end")
    if input('exit? (y/n)').lower() == 'y':
        break

# puzzle_size = 3
# puzzle = [ x for x in range(puzzle_size**2)]
# puzzle = np.reshape(np.array(puzzle), (3, 3))

# x_pos, y_pos = 0, 0 # x_pos : row, y_pos : column
# shake_forward = []

# # puzzle init
# for i in range(100):
#     mv = random.randint(0, 3)

#     if mv == 0: # up
#         try:
#             x_pos -= 1
#             if x_pos < 0: raise
#             shake_forward.append(mv)
#             temp = puzzle[x_pos+1][y_pos]
#             puzzle[x_pos+1][y_pos] = puzzle[x_pos][y_pos]
#             puzzle[x_pos][y_pos] = temp
#             print(mv, puzzle, end="\n\n")
#         except:
#             x_pos += 1

#     if mv == 1: # left
#         try:
#             y_pos -= 1
#             if y_pos < 0 : raise
#             shake_forward.append(mv)
#             temp = puzzle[x_pos][y_pos+1]
#             puzzle[x_pos][y_pos+1] = puzzle[x_pos][y_pos]
#             puzzle[x_pos][y_pos] = temp
#             print(mv, puzzle, end="\n\n")
#         except:
#             y_pos += 1

#     if mv == 2: # right
#         try:
#             y_pos += 1
#             if y_pos >= puzzle_size: raise
#             shake_forward.append(mv)
#             temp = puzzle[x_pos][y_pos-1]
#             puzzle[x_pos][y_pos-1] = puzzle[x_pos][y_pos]
#             puzzle[x_pos][y_pos] = temp
#             print(mv, puzzle, end="\n\n")
#         except:
#             y_pos -= 1

#     if mv == 3: # down
#         try:
#             x_pos += 1
#             if x_pos >= puzzle_size: raise
#             shake_forward.append(mv)
#             temp = puzzle[x_pos-1][y_pos]
#             puzzle[x_pos-1][y_pos] = puzzle[x_pos][y_pos]
#             puzzle[x_pos][y_pos] = temp
#             print(mv, puzzle, end="\n\n")
#         except:
#             x_pos -= 1

# 3 - mv == offsite movement

# def printForward(arr):
#     print("[", end="")
#     for data in arr:
#         if data == 0:
#             data = "u"
#         if data == 1:
#             data = "l"
#         if data == 2:
#             data = "r"
#         if data == 3:
#             data = "d"
#         print(data, end=",")
#     print("]")


# # movement optimize
# x_f = False
# for _ in range(100):
#     printForward(shake_forward)
#     for idx, data in enumerate(shake_forward[:-1]):
#         if (3 - shake_forward[idx+1] == data):
#             shake_forward.pop(idx+1)
#             shake_forward.pop(idx)
#             x_f = False
#             break
#         x_f = True
#     if x_f:
#         break

# def mv_up():
#     global x_pos, y_pos, puzzle, shake_forward
#     try:
#         x_pos -= 1
#         if x_pos < 0: raise
#         if 3 - shake_forward[-1] == 0:
#             shake_forward.pop(-1)
#         else:
#             shake_forward.push(0)
#         temp = puzzle[x_pos+1][y_pos]
#         puzzle[x_pos+1][y_pos] = puzzle[x_pos][y_pos]
#         puzzle[x_pos][y_pos] = temp
#         print(mv, puzzle, end="\n\n")
#     except:
#         x_pos += 1

# def mv_down():
#     global x_pos, y_pos, puzzle, shake_forward
#     try:
#         x_pos -= 1
#         if x_pos >= puzzle_size: raise
#         if 3 - shake_forward[-1] == 3:
#             shake_forward.pop(-1)
#         else:
#             shake_forward.push(3)
#         temp = puzzle[x_pos-1][y_pos]
#         puzzle[x_pos-1][y_pos] = puzzle[x_pos][y_pos]
#         puzzle[x_pos][y_pos] = temp
#         print(mv, puzzle, end="\n\n")
#     except:
#         x_pos += 1

# def mv_left():
#     global x_pos, y_pos, puzzle, shake_forward
#     try:
#         y_pos -= 1
#         if y_pos < 0: raise
#         if 3 - shake_forward[-1] == 1:
#             shake_forward.pop(-1)
#         else:
#             shake_forward.push(1)
#         temp = puzzle[x_pos][y_pos+1]
#         puzzle[x_pos][y_pos+1] = puzzle[x_pos][y_pos]
#         puzzle[x_pos][y_pos] = temp
#         print(mv, puzzle, end="\n\n")
#     except:
#         x_pos += 1

# def mv_right():
#     global x_pos, y_pos, puzzle, shake_forward
#     try:
#         y_pos += 1
#         if y_pos >= puzzle_size: raise
#         if 3 - shake_forward[-1] == 2:
#             shake_forward.pop(-1)
#         else:
#             shake_forward.push(2)
#         temp = puzzle[x_pos][y_pos-1]
#         puzzle[x_pos][y_pos-1] = puzzle[x_pos][y_pos]
#         puzzle[x_pos][y_pos] = temp
#         print(mv, puzzle, end="\n\n")
#     except:
#         y_pos -= 1

# def on_press(key):
#     print(key)
#     print(puzzle)
#     if key == keyboard.Key.up:
#         mv_up()
#     if key == keyboard.Key.down:
#         mv_down()
#     if key == keyboard.Key.left:
#         mv_left()
#     if key == keyboard.Key.right:
#         mv_right()

#     if key == keyboard.Key.esc:
#         return False


# with keyboard.Listener(on_press=on_press) as listener:
#     listener.join()