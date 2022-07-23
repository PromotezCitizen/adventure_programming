from collections import deque
import threading
import random

MAX_TIME = 30
QUEUE_SIZE = 5

class Queue():
    def __init__(self):
        self.__max_size = QUEUE_SIZE
        self.__queue = []
        None

    def enqueue(self, data):
        self.__queue.append(data)
    
    def dequeue(self):
        return self.__queue.pop(0)

    def addWaitTime(self):
        for data in self.__queue:
            data[-1] += 1

    def isFull(self):
        return len(self.__queue) == self.__max_size

    def isEmpty(self):
        return len(self.__queue) == 0

    def print(self):
        print(self.__queue)
        for idx, data in enumerate(self.__queue):
            print(idx, data)

# 공유된 변수를 위한 클래스
class ThreadLocks():
    def __init__(self):
        self._queue_lock = threading.Lock()
        global arr

class ThreadVariable(ThreadLocks): # runner
    def __init__(self):
        super().__init__()
        self.turn = 0
        global dequeue_arr

    def run(self):
        for _ in range(1, 11):
            self._queue_lock.acquire()
            choice = random.randrange(1, 7)
            if choice == 1: # 매장 방문
                data = [self.turn, random.randint(1, 10), 0] # arrival time, service time, wait time
                self.__enqueueFrontData(data)

            elif choice == 4: # call
                # 전화가 온 경우에는 queue에서 빼지 않는다.
                data = [self.turn, random.randint(1, 10), 0] # arrival time, service time, wait time
                arr.addWaitTime()
                self.__enqueueCallData(data)
                continue
            
            # 시간 지났는지 조건 판단 가능해야함
            deq_data = self.__dequeueData()
            if deq_data is not None:
                dequeue_arr.append(deq_data)
            self._queue_lock.release()

    def __enqueueFrontData(self, data):
        if not arr.isFull():
            arr.enqueue(data)
            self.__enqueuePrint(data)
            self.turn += 1
        else:
            print("user fulled. cant append call user")

    def __enqueueCallData(self, data):
        if not arr.isFull():
            arr.enqueue(data)
            self.__enqueuePrint(data)
            self.turn += 1
        else:
            print("user fulled. cant append call user")

    def __dequeueData(self):
        if not arr.isEmpty():
            deq_data = arr.dequeue()
            self.__dequeuePrint(deq_data)
            return deq_data
        return None

    def __enqueuePrint(self, data):
        print('enqueue - user: %2d, data: %2d' % (data[0], data[1]))

    def __dequeuePrint(self, data):
        print('dequeue - user: %2d, data: %2d' % (data[0], data[1]))
 
# ConsumerThread
class ConsumerThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.name = "consumer"
        global runner
 
    # ConsumerThread가 실행하는 함수
    def run(self):
        runner.run()
 
arr = Queue()
dequeue_arr = []

runner = ThreadVariable()

for _ in range(2):
    th = ConsumerThread()
    th.start()

mainThread = threading.current_thread()
for thread in threading.enumerate():
    if thread is not mainThread:
        thread.join()

finish = runner.turn
print(finish)
print(dequeue_arr)