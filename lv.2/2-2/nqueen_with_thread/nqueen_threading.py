from nqueen import NQueen
import threading
import time

class NQueenThread(threading.Thread):
    def __init__(self, map_size, calc_range):
        threading.Thread.__init__(self, name='NQueenThread')
        self._nqueen = NQueen(map_size, calc_range)
        self._result = None
        self._unique_result = None

    def run(self):
        self._result = self._nqueen.run()

    def join(self):
        # join 함수 overriding. 권장하지는 않는다고 한다.
        threading.Thread.join(self)
        return self._result

def useThreading(map_size, splited):
    thread_pool = []
    nqueen_result_list = []
    start_time = time.perf_counter()

    for arr in splited:
        nqueen_thread = NQueenThread(map_size, arr)
        thread_pool.append(nqueen_thread)
        nqueen_thread.start()

    for thread in thread_pool:
        nqueen_result = thread.join()
        for result in nqueen_result:
            nqueen_result_list.append(result)

    print(f"time elapsed : {int(round((time.perf_counter() - start_time) * 1000))}ms")
    print('results: %6d' % (len(nqueen_result_list)))