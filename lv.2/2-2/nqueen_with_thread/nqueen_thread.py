from nqueen import NQueen
import threading

class NQueenThread(threading.Thread):
    def __init__(self, map_size, calc_range):
        self._nqueen = NQueen(map_size, calc_range)
        self._result = None
        self._unique_result = None

    def run(self):
        self._result, self._unique_result = self._nqueen.run()

    def join(self):
        # join 함수 overriding. 권장하지는 않는다고 한다.
        threading.Thread.join(self)
        return self._result, self._unique_result