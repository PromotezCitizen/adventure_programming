import random
import time

class Beetle():
    def __init__(self, map_size, calc_range, num_roach):
        self._map_size = map_size
        self._calc_range = calc_range
        self._num_roach = num_roach
        self._UP = 0
        self._LEFT = 1
        self._DOWN = 2
        self._RIGHT = 3
        self._return_data = []

    def start(self):
        for calc in self._calc_range:
            self._return_data.append(self.run())
        return self._return_data

    def run(self):
        beetle_map = [ [ 0 for _ in range(self._map_size) ] for _ in range(self._map_size) ]
        beetle_pos = [ {
                'row':random.randint(0, self._map_size-1),
                'col':random.randint(0, self._map_size-1)
            } for _ in range(self._num_roach) ]
        beetle_move = [ 0 for _ in range(4) ]
        beetle_move_real = [ 0 for _ in range(4) ]
        # 딱정벌레가 이동한 것은 한 번에 계산
        # 따로 계산하면 그만큼 오버헤드 발생
        mv, mv_real = 0, 0

        start = time.perf_counter()
        while self._checkRunDone(beetle_map) != self._map_size**2:
            # 해당 턴의 모든 딱정벌레가 다 이동해야 모든 곳을 이동했는지 여부를 계산
            #   why? 조건 한 번 검사할때마다 많은 오버헤드
            for position in beetle_pos:
                direct = random.randint(0,3)
                mv += 1
                beetle_move[direct] += 1
                if self._checkPossibilityNMove(direct, position, self._map_size):
                    mv_real += 1
                    beetle_move_real[direct] += 1
                    beetle_map[position['row']][position['col']] = 1
        end = time.perf_counter()
        return {'mv': mv, 'mv_real': mv_real, 'runtime': end-start, 'direct': beetle_move, 'direct_real': beetle_move_real}

    def _checkRunDone(self, beetle_map):
        # 맵 전체를 다 돌았는지를 배열 sum값으로 판단
        return sum([ sum(x) for x in beetle_map ])

    def _checkPossibilityNMove(self, mv, beetle_pos, map_size):
        if mv == self._UP:
            if beetle_pos['row'] == 0:
                return False
            beetle_pos['row'] -= 1
            return True
        if mv == self._LEFT:
            if beetle_pos['col'] == 0:
                return False
            beetle_pos['col'] -= 1
            return True
        if mv == self._DOWN:
            if beetle_pos['row'] == map_size - 1:
                return False
            beetle_pos['row'] += 1
            return True
        if mv == self._RIGHT:
            if beetle_pos['col'] == map_size - 1:
                return False
            beetle_pos['col'] += 1
            return True

