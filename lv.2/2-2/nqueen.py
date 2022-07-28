import copy

class NQueen():
    def __init__(self, size):
        self._size = size
        self._chess_map = [ [0 for _ in range(size)] for _ in range(size)]
        self._results = []
        self._unique_results = []

    def run(self):
        self._solve(self._chess_map, 0)
        self._getUniqueResults()
        self._printResults("", self._results)
        self._printResults("unique ", self._unique_results)

    def _printResults(self, msg, arr): # msg="" or "unique "
        print('%sresults - %5d' % (msg, len(arr)))
        # self._printFlag(arr)

    def _printFlag(self, arr):
        if len(arr) == 0:
            print("결과 없음")
        else:
            for idx, chess_map in enumerate(arr):
                self._printChessMap(idx, chess_map)

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
        ]  # abs 쓰는 방법도 있다

        cross_map_1_to_7 = [
            x[check_pos - idx] 
            for idx, x in enumerate(chess_map)
            if (check_pos - idx < self._size) and (idx < pos_row)
        ]  # abs 쓰는 방법도 있다

        # print('pos - row: %2d, col: %2d' % (pos_row, pos_col))
        # print('vertical -', vertical_map)
        # print('11 to 5 -', cross_map_11_to_5)
        # print('1 to 7 -', cross_map_1_to_7)

        result = sum(vertical_map) + sum(cross_map_11_to_5) + sum(cross_map_1_to_7)
        if result == 0:
            return True
        return False

    def _solve(self, chess_map, pos_row):
        local_map = copy.deepcopy(chess_map)
        if pos_row >= self._size:
            self._results.append(local_map)
            # self._printChessMap(0, local_map)
            return
        for idx in range(self._size):
            if not self._calcCanPosition(local_map, pos_row, idx):
                continue
            local_map[pos_row][idx] = 1
            # self._printChessMap(0, local_map)
            self._solve(local_map, pos_row+1)
            local_map[pos_row][idx] = 0

    def _getUniqueResults(self):
        self._unique_results = copy.deepcopy(self._results)
        for arr in self._unique_results:
            self._isTrun2RightIn(arr)

    def _isTrun2RightIn(self,arr):
        data = copy.deepcopy(arr)
        for _ in range(3):
            data = [ list(reversed([x[col] for x in data])) for col in range(map_size) ]
            try:
                self._unique_results.remove(data)
            except:
                None

if __name__ == "__main__":
    map_size = 4
    queen = NQueen(map_size)

    queen.run()
