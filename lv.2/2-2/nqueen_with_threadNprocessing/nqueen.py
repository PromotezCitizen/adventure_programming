import copy

class NQueen():
    def __init__(self, map_size, calc_range):
        self._size = map_size
        self._calc_range = calc_range
        self._chess_map = [ [0 for _ in range(self._size)] for _ in range(self._size)]
        self._results = []

    def run(self):
        if len(self._calc_range) > 0:
            self._solve(self._chess_map, 0)

        return self._results

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

        result = sum(vertical_map) + sum(cross_map_11_to_5) + sum(cross_map_1_to_7)
        if result == 0:
            return True
        return False

    def _solve(self, chess_map, pos_row):
        local_map = copy.deepcopy(chess_map)
        if pos_row >= self._size:
            self._results.append(local_map)
            return
        for idx in range(self._size):
            if (pos_row == 0) and (idx not in self._calc_range):
                continue  # 자신이 맡은 인덱스가 아니라면 건너뛴다
            if not self._calcCanPosition(local_map, pos_row, idx):
                continue
            local_map[pos_row][idx] = 1
            self._solve(local_map, pos_row+1)
            local_map[pos_row][idx] = 0