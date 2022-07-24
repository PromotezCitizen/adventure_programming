import time
import random
import numpy as np
import os

class NPuzzle():
    def __init__(self, puzzle_size):
        self._puzzle_size = puzzle_size
        self._puzzle = [ x for x in range(self._puzzle_size**2)]
        self._puzzle = np.reshape(np.array(self._puzzle), (self._puzzle_size, self._puzzle_size))
        self._shake_forward = []
        self._x_pos = 0
        self._y_pos = 0
        self._puzzle_init()
        self._optimize_com_movement()

    def _puzzle_init(self):
        for _ in range(100):
            mv = random.randint(0, 3)
            if mv == 0: # up
                try:
                    self._x_pos -= 1
                    if self._x_pos < 0: raise
                    self._shake_forward.append(mv)
                    self._change_position([self._x_pos+1, self._y_pos], [self._x_pos, self._y_pos])
                except:
                    self._x_pos += 1

            elif mv == 1: # left
                try:
                    self._y_pos -= 1
                    if self._y_pos < 0 : raise
                    self._shake_forward.append(mv)
                    self._change_position([self._x_pos, self._y_pos+1], [self._x_pos, self._y_pos])
                except:
                    self._y_pos += 1

            elif mv == 2: # right
                try:
                    self._y_pos += 1
                    if self._y_pos >= self._puzzle_size: raise
                    self._shake_forward.append(mv)
                    self._change_position([self._x_pos, self._y_pos-1], [self._x_pos, self._y_pos])
                except:
                    self._y_pos -= 1

            else: # down
                try:
                    self._x_pos += 1
                    if self._x_pos >= self._puzzle_size: raise
                    self._shake_forward.append(mv)
                    self._change_position([self._x_pos-1, self._y_pos], [self._x_pos, self._y_pos])
                except:
                    self._x_pos -= 1

    def _optimize_com_movement(self):
        x_f = False
        for _ in range(100):
            #self._print_forward()
            for idx, data in enumerate(self._shake_forward[:-1]):
                if (3 - self._shake_forward[idx+1] == data):
                    self._shake_forward.pop(idx+1)
                    self._shake_forward.pop(idx)
                    x_f = False
                    break
                x_f = True
            if x_f:
                break

    def _print_forward(self):
        print("[", end="")
        for data in self._shake_forward:
            if   data == 0: data = "u"
            elif data == 1: data = "l"
            elif data == 2: data = "r"
            else          : data = "d"
            print(data, end=",")
        print("]")

    def _mv_forward_push(self, dir):
        if 3 - self._shake_forward[0] == dir:
            self._shake_forward.pop(0)
        else:
            self._shake_forward.insert(0, dir)

    def _change_position(self, origin, to): # _change_postion(origin: [x_pos,y_pos], to: [x_pos,y_pos])
        temp = self._puzzle[origin[0]][origin[1]]
        self._puzzle[origin[0]][origin[1]] = self._puzzle[to[0]][to[1]]
        self._puzzle[to[0]][to[1]] = temp

'''
    def _puzzle_map(self, rowsize, flag):
        maps = [['┌', '┐', '━'], ['└', '┘', '━'], ['│', '│', ' ']]
        temp = [maps[flag][2] for _ in range(rowsize + (self._puzzle_size*3+1))]
        temp.insert(0, maps[flag][0])
        temp.append(maps[flag][1])
        return temp

    def _get_puzzle_row_size(self):
        rowsize = self._puzzle_size
        if self._puzzle_size**2 < 10:rowsize *= 1
        elif self._puzzle_size**2 < 100: rowsize *= 2
        elif self._puzzle_size**2 < 1000: rowsize *= 3
        return rowsize

    def print_puzzle(self):
        os.system('cls')
        print('player 1) 이동 : ↑←↓→, 힌트 : i, 세이브 : o, 로드 : p, 종료 : esc') # 기본 조작법
        print('player 2) 이동 : wasd, 힌트 : 1, 세이브 : 2, 로드 : 3, 종료 : esc')
        # 3*3
        # row : ┌ ┐ => 2, print value : puzzle_size, blank : puzzle_size+1
        # col : ┌ ┐ => 2, print value : puzzle_size, blank : puzzle_size+1
        # 3*3 => (2+3+(3+1))*(2+3+(3+1)) == 9*9
        
        # 4*4
        # row : ┌ ┐ => 2, print value : puzzle_size*2, blank : puzzle_size+1
        # col : ┌ ┐ => 2, print value : puzzle_size, blank : puzzle_size+1
        # 4*4 => (2+4*2+(3+1))*(2+4+(3+1)) == 14*10

        rowsize = self._get_puzzle_row_size()

        dat = []
        for s_arr in self._puzzle:
            temp = []
            for data in s_arr:
                if self._puzzle_size**2 < 10:
                    if data == 0:
                        temp.append(' {0:1s} '.format('◎'))
                        continue
                    temp.append(' {0:1d} '.format(data))
                elif self._puzzle_size**2 < 100:
                    if data == 0:
                        temp.append(' {0:2s} '.format('◎'))
                        continue
                    temp.append(' {0:2d} '.format(data))
                elif self._puzzle_size**2 < 1000:
                    if data == 0:
                        temp.append(' {0:3s} '.format('◎'))
                        continue
                    temp.append(' {0:3d} '.format(data))
            dat.append(temp)
        # rowsize * strlen
        
        header = self._puzzle_map(rowsize, 0)
        footer = self._puzzle_map(rowsize, 1)
        spliter = self._puzzle_map(rowsize, 2)

        print(''.join(header))
        print(''.join(spliter))
        for datas in dat:
            datas.insert(0, '│')
            datas.append('│')
            print(' '.join(datas))
            print(''.join(spliter))
            None
        print(''.join(footer))
'''

class NPuzzleRunner(NPuzzle):
    def __init__(self, size, idx):
        super().__init__(size, idx)
        self._hint = 4
        self._max_hint = self._hint
        self.__move = ['Up', 'Left', 'Right', 'Down']
        self._save_name = 'save{0}.npy'.format(idx)

    def mv_start(self):
        self._shake_forward.reverse()
        return self._puzzle

    def mv_end(self):
        if len(self._shake_forward) == 0:
            return True
        temp = [ x for x in range(self._puzzle_size**2) ]
        temp = np.resize(np.array(temp), (3,3))
        if np.array_equal(temp, self._puzzle):
            return True
        return False

    def auto_move(self):
        for _ in range(len(self._shake_forward)):
            mv = self._shake_forward[0]
            if mv == 0: # shaked to up -> restore: down
                self.mv_down()
            elif mv == 1: # shaked to left -> restore: right
                self.mv_right()
            elif mv == 2: # shaked to right -> restore: left
                self.mv_left()
            elif mv == 3: # shaked to up -> restore: up
                self.mv_up()
            print('move to ', self.__move[3-mv])
            time.sleep(1)

        return self.mv_end()

    def hint(self):
        if self._hint < 1:
            return 'Not available hint: you have zero hint coin'
        data = 3 - self._shake_forward[0]
        self._hint -= 1
        msg = " - hint coin left (%d/%d)" % (self._hint, self._max_hint)
        if data == 0: return "UP" + msg
        if data == 1: return "LEFT" + msg
        if data == 2: return "RIGHT" + msg
        else        : return "DOWN" + msg

    def mv_up(self):
        try:
            self._x_pos -= 1
            if self._x_pos < 0: raise Exception
            self._mv_forward_push(0)
            self._change_position([self._x_pos+1, self._y_pos], [self._x_pos, self._y_pos])
        except Exception as e:
            self._x_pos += 1

        return self.mv_end(), self._puzzle

    def mv_down(self):
        try:
            self._x_pos += 1
            if self._x_pos >= self._puzzle_size: raise Exception
            self._mv_forward_push(3)
            self._change_position([self._x_pos-1, self._y_pos], [self._x_pos, self._y_pos])
        except Exception as e:
            self._x_pos -= 1

        return self.mv_end(), self._puzzle

    def mv_left(self):
        try:
            self._y_pos -= 1
            if self._y_pos < 0: raise Exception
            self._mv_forward_push(1)
            self._change_position([self._x_pos, self._y_pos+1], [self._x_pos, self._y_pos])
        except Exception as e:
            self._y_pos += 1

        return self.mv_end(), self._puzzle

    def mv_right(self):
        try:
            self._y_pos += 1
            if self._y_pos >= self._puzzle_size: raise Exception
            self._mv_forward_push(2)
            self._change_position([self._x_pos, self._y_pos-1], [self._x_pos, self._y_pos])
        except Exception as e:
            self._y_pos -= 1

        return self.mv_end(), self._puzzle

    def save(self):
        # user count
        # ┠ row, column
        # ┠ left hint counts
        # ┠ puzzle
        # ┗ computer calculate arr
        try:
            temp = np.array([np.array([self._y_pos, self._x_pos]), np.array(self._hint), self._puzzle, np.array(self._shake_forward)], dtype=object)
            np.save(self._save_name, temp)
            print('save finished')
        except Exception as e:
            print('save error', e)

    def load(self):
        try:
            t = np.load(self._save_name, allow_pickle=True)
            if len(t) != 4:
                raise Exception
            if len(t[0]) != 2:
                raise Exception
            pos = t[0]
            self._y_pos = pos[0]
            self._x_pos = pos[1]
            self._hint = t[1]
            self._puzzle = t[2]
            self._shake_forward = t[3].tolist()
            self._puzzle_size = len(t[2])

            print('load finished')
            return self._puzzle
        except Exception as e:
            print('savefile error', e)
            return None


class NPuzzlePrinter(NPuzzle):
    def __init__(self, players):
        self.__player_maps = players
        self._puzzle_size = len(self.__player_maps[0])

    def update_map(self, idx, map):
        self.__player_maps[idx] = map
        self.print_puzzle()

    def _puzzle_map_template(self, rowsize, flag):
        maps = [['┌', '┐', '─'], ['└', '┘', '─'], ['│', '│', ' ']]
        temp = [maps[flag][2] for _ in range(rowsize + (self._puzzle_size*3+1))]
        temp.insert(0, maps[flag][0])
        temp.append(maps[flag][1])
        if len(self.__player_maps) == 2:
            temp.append('    ')
            temp2 = [maps[flag][2] for _ in range(rowsize + (self._puzzle_size*3+1))]
            temp.append(maps[flag][0])
            temp += temp2
            temp.append(maps[flag][1])
        return temp

    def _get_puzzle_row_size(self):
        rowsize = self._puzzle_size
        if self._puzzle_size**2 < 10:rowsize *= 1
        elif self._puzzle_size**2 < 100: rowsize *= 2
        elif self._puzzle_size**2 < 1000: rowsize *= 3
        return rowsize

    def _create_puzzle_position(self):
        players_map = []
        for puzzle in self.__player_maps:
            dat = []
            for s_arr in puzzle:
                temp = []
                for data in s_arr:
                    if self._puzzle_size**2 < 10:
                        if data == 0:
                            temp.append(' {0:1s} '.format('◎'))
                            continue
                        temp.append(' {0:1d} '.format(data))
                    elif self._puzzle_size**2 < 100:
                        if data == 0:
                            temp.append(' {0:2s} '.format('◎'))
                            continue
                        temp.append(' {0:2d} '.format(data))
                    elif self._puzzle_size**2 < 1000:
                        if data == 0:
                            temp.append(' {0:3s} '.format('◎'))
                            continue
                        temp.append(' {0:3d} '.format(data))
                    else :
                        if data == 0:
                            temp.append(' {0:4s} '.format('◎'))
                            continue
                        temp.append(' {0:4d} '.format(data))
                dat.append(temp)
            players_map.append(dat)
        return players_map

    def _print_puzzle_pretty(self, players_map, header, spliter, footer):
        print(''.join(header))
        print(''.join(spliter))
        for idx_row, _ in enumerate(players_map[0]):
            for idx in range(len(players_map)):
                players_map[idx][idx_row].insert(0, '│')
                players_map[idx][idx_row].append('│')
                print(' '.join(players_map[idx][idx_row]), end="    ")
            print('', end='\n')
            print(''.join(spliter))
        print(''.join(footer))

    def print_puzzle(self):
        os.system('cls')
        print("player 1) 이동 : wasd, 힌트 : `, 세이브 : 2, 로드 : 3, 종료 : esc") # 기본 조작법
        if len(players_map) == 2:
            print('player 2) 이동 : ↑←↓→, 힌트 : u, 세이브 : o, 로드 : p, 종료 : esc')
        
        # 맵 생성 규칙 정의
        # 3*3
        # row : ┌ ┐ => 2, print value : puzzle_size, blank : puzzle_size+1
        # col : ┌ ┐ => 2, print value : puzzle_size, blank : puzzle_size+1
        # 3*3 => (2+3+(3+1))*(2+3+(3+1)) == 9*9
        
        # 4*4
        # row : ┌ ┐ => 2, print value : puzzle_size*2, blank : puzzle_size+1
        # col : ┌ ┐ => 2, print value : puzzle_size, blank : puzzle_size+1
        # 4*4 => (2+4*2+(3+1))*(2+4+(3+1)) == 14*10

        # 10*10
        # row : ┌ ┐ => 2, print value : puzzle_size*3, blank : puzzle_size+1
        # col : ┌ ┐ => 2, print value : puzzle_size, blank : puzzle_size+1
        # 4*4 => (2+10*3+(3+1))*(2+10+(3+1)) == 36*16

        rowsize = self._get_puzzle_row_size()

        players_map = self._create_puzzle_position()
        
        header = self._puzzle_map_template(rowsize, 0)
        footer = self._puzzle_map_template(rowsize, 1)
        spliter = self._puzzle_map_template(rowsize, 2)

        self._print_puzzle_pretty(players_map, header, spliter, footer)