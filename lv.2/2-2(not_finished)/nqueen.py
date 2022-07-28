import random
import copy

class NQueen():
    def __init__(self, size):
        self._size = size
        self.__temp = [0,1]
        self._chess_map = [ [random.choices(self.__temp, weights=[4,1])[0] for _ in range(size)] for _ in range(size)]
        self._results = []

    def run(self):
        self._move(self._chess_map, 0)
        # self._calcCanPosition(self._chess_map, 3, 2)
        self._printResults()

    def _printResults(self):
        print(self._results)
        # if len(self._results) == 0:
        #     print("결과 없음")
        # else:
        #     for idx, chess_map in enumerate(self._results):
        #         self._printChessMap(idx, chess_map)

    def _printChessMap(self, idx, chess_map):
        print('result %3d' % idx)
        for x in chess_map:
            for data in x:
                print('%2d' % data, end=" ")
            print('')
        print('')

    def _calcCanPosition(self, chess_map, pos_row, pos_col):
        check_neg = pos_col - pos_row
        check_pos = pos_row + pos_col

        vertical_map = [
            x[pos_col]
            for idx, x in enumerate(chess_map)
            if (idx < pos_row)
        ]

        cross_map_11_to_5 = [
            x[check_neg + idx]
            for idx, x in enumerate(chess_map)
            if (check_neg + idx > -1) and (idx < pos_row)
        ]

        cross_map_1_to_7 = [
            x[check_pos - idx] 
            for idx, x in enumerate(chess_map)
            if (check_pos - idx < self._size) and (idx < pos_row)
        ]

        # print('pos - row: %2d, col: %2d' % (pos_row, pos_col))
        # print('vertical -', vertical_map)
        # print('11 to 5 -', cross_map_11_to_5)
        # print('1 to 7 -', cross_map_1_to_7)

        result = sum(vertical_map) + sum(cross_map_11_to_5) + sum(cross_map_1_to_7)
        if result == 0:
            return True
        return False

    def _move(self, chess_map, pos_row):
        local_map = copy.deepcopy(chess_map)
        if pos_row >= self._size:
            self._results.append(local_map)
            self._printChessMap(0, local_map)
            return
        for idx in range(self._size):
            if not self._calcCanPosition(local_map, pos_row, idx): continue
            print(pos_row, idx)
            local_map[pos_row][idx] = 1
            self._move(local_map, pos_row+1)
            local_map[pos_row][idx] = 0


def Move(chess_map, pos_row):
    local_map = copy.deepcopy(chess_map)
    if pos_row >= size:
        results.append(local_map)
        return
    for idx in range(size):
        if not calcCanPosition(local_map, pos_row, idx): continue
        local_map[pos_row][idx] = 1
        Move(local_map, pos_row+1)
        local_map[pos_row][idx] = 0

# map_size = 4
# queen = NQueen(map_size)

# queen.run()



def t():
    def calcCanPosition(chess_map, pos_row, pos_col):
        check_neg = pos_col - pos_row
        check_pos = pos_row + pos_col

        vertical_map = [
            x[pos_col]
            for idx, x in enumerate(chess_map)
            if (idx < pos_row)
        ]

        cross_map_11_to_5 = [
            x[check_neg + idx]
            for idx, x in enumerate(chess_map)
            if (check_neg + idx > -1) and (idx < pos_row)
        ]

        cross_map_1_to_7 = [
            x[check_pos - idx] 
            for idx, x in enumerate(chess_map)
            if (check_pos - idx < size) and (idx < pos_row)
        ]

        # print('pos - row: %2d, col: %2d' % (pos_row, pos_col))
        # print('vertical -', vertical_map)
        # print('11 to 5 -', cross_map_11_to_5)
        # print('1 to 7 -', cross_map_1_to_7)

        result = sum(vertical_map) + sum(cross_map_11_to_5) + sum(cross_map_1_to_7)
        if result == 0:
            return True
        return False

    def printMap(chess_map):
        for x in chess_map:
            for data in x:
                print('%2d' % data, end=" ")
            print('')
        print('')

    def Move(chess_map, pos_row):
        local_map = copy.deepcopy(chess_map)
        if pos_row >= size:
            results.append(local_map)
            return
        for idx in range(size):
            if not calcCanPosition(local_map, pos_row, idx): continue
            local_map[pos_row][idx] = 1
            Move(local_map, pos_row+1)
            local_map[pos_row][idx] = 0

    size = 4
    results = []
    chess_map = [ [ 0 for _ in range(size) ] for _ in range(size) ]
    for x in chess_map:
        print(x)
    print('')

    Move(chess_map, 0)

    for arr in results:
        printMap(arr)

t()
