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
        print('\t\t', self.__queue)

# 공유된 변수를 위한 클래스
class ThreadVariable(): # runner
    def __init__(self):
        global queue
        global queue_lock
        global customer_idx
        self._dequeue_arr = []
        self.__service_time_left = 0

    def run(self):
        for arrival in range(MAX_TIME):

            queue_lock.acquire()
            choice = random.randrange(1, 7)
            print('switches - %d(%2d)' % (choice, arrival))
            data = [customer_idx, arrival, random.randint(1, 10), 0] # user idx, arrival time, service time, wait time
            if choice == 1: # 매장 방문
                self.__enqueueData(data, 'front')
            elif choice == 4: # call
                queue.addWaitTime()
                self.__enqueueData(data, 'call')
                if self.__service_time_left != 0:
                    self._dequeue_arr[-1][-1] = +1
                    queue_lock.release()
                    continue
            queue_lock.release()

            queue_lock.acquire()
            print(self.__service_time_left)
            if self.__service_time_left == 0:
                deq_data = self.__dequeueData()
                if deq_data is not None:
                    self._dequeue_arr.append(deq_data)
                    self.__service_time_left = deq_data[2]
                    queue.addWaitTime()
            else:
                self.__service_time_left -= 1
                queue.addWaitTime()
            queue_lock.release()

        return self._dequeue_arr

    def __enqueueData(self, data, msg):
        global customer_idx
        if not queue.isFull():
            queue.enqueue(data)
            customer_idx += 1
            self.__enqueuePrint(data, msg)
        else:
            print("\tuser fulled. cant append %s user" % msg)
        queue.print()

    def __dequeueData(self):
        if not queue.isEmpty():
            deq_data = queue.dequeue()
            self.__dequeuePrint(deq_data)
            queue.print()
            return deq_data
        print("\tuser dequeue failed. empty queue")
        queue.print()
        return None

    def __enqueuePrint(self, data, msg):
        print('\tenqueue(%5s) - user: %2d, arrival : %2d, data: %2d' % (msg, data[0], data[1], data[2]))

    def __dequeuePrint(self, data):
        print('\tdequeue - user: %2d, arrival : %2d, data: %2d' % (data[0], data[1], data[2]))
 
# ConsumerThread
class ConsumerThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.name = "consumer"
        self._return = None
        global runner
 
    # ConsumerThread가 실행하는 함수
    def run(self):
        self._return = runner.run()

    def join(self):
        threading.Thread.join(self)
        return self._return
 
queue = Queue()
customer_idx = 0
result = None

queue_lock = threading.Lock()

runner = ThreadVariable()

for _ in range(2):
    th = ConsumerThread()
    th.start()

mainThread = threading.current_thread()
for thread in threading.enumerate():
    if thread is not mainThread:
        result = thread.join()

print(result)