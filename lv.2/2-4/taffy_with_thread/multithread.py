import threading
import random

from taffy_queue import Queue
from err import NotNumErr, NumRngErr

MAX_TIME = 20
QUEUE_SIZE = 5

# Taffy 대기열 계산을 위한 대기열
class ThreadVariable(): # runner
    def __init__(self, time):
        self._dequeue_arr = []
        self.__service_time_left = 0
        self._max_time = time
        global queue
        global queue_lock
        global customer_idx

    # 한 턴에 한 명의 고객이 온다고 가정한다.
    # 전화를 한 턴은 모든 고객이 한 턴을 쉰다.
    def run(self):
        for arrival in range(self._max_time):
            queue_lock.acquire() # mutex lock 이용, 큐에 여러 스레드가 동시에 접근하지 못하도록 막는다.
            choice = random.randrange(1, 7)
            data = [customer_idx, arrival, random.randint(1, 10), 0] # user idx, arrival time, service time, wait time
            if choice == 1: # 매장 방문
                print('switches - %d(%2d)' % (choice, arrival))
                self.__enqueueData(data, 'front')
            elif choice == 4: # 전화 예약
                print('switches - %d(%2d)' % (choice, arrival))
                queue.addWaitTime() # 전화가 온 경우 모든 인원 대기시간 증가.
                self.__enqueueData(data, 'call')
                if self.__service_time_left != 0: # 창구에 인원이 있다면 해당 인원의 대기시간 1 증가
                    self._dequeue_arr[-1][-1] = +1
                    queue_lock.release() # lock 해제하지 않고 continue시 deadlock 발생
                    continue
            queue_lock.release()

            queue_lock.acquire()
            print(self.__service_time_left)
            if self.__service_time_left == 0: # 창구에 사람이 없는 경우 고객을 창구로 불러온다
                deq_data = self.__dequeueData()
                if deq_data is not None: # 대기열에 고객이 있는 경우에만 창구로 불러온다
                    # user idx, arrival time, service time, wait time
                    #                       ↓ (변환)
                    # user idx, arrival time,'service start time', service time, wait time
                    deq_data.insert(2, arrival) # 개별 고객 출력 시 서비스 시작시간도 출력해야 함
                    self._dequeue_arr.append(deq_data)
                    self.__service_time_left = deq_data[-2] # 해당 고객의 서비스 시작 및
                                                            # 서비스 남은 시간 저장
                    queue.addWaitTime()
            else:
                self.__service_time_left -= 1
                queue.addWaitTime() # 대기시간 증가
            queue_lock.release()

        return self._dequeue_arr

    def __enqueueData(self, data, msg):
        global customer_idx
        if not queue.isFull(): # 큐가 다 찬 상태가 아닌 경우에 실행
            queue.enqueue(data)
            customer_idx += 1
            self.__enqueuePrint(data, msg)
        else:
            print("\tuser fulled. cant append %s user" % msg)
        queue.print()

    def __dequeueData(self):
        if not queue.isEmpty(): # 큐가 비어있지 않은 경우에 실행
            deq_data = queue.dequeue()
            self.__dequeuePrint(deq_data)
            queue.print()
            return deq_data
        print("\tuser dequeue failed. empty queue")
        queue.print()
        return None

    def __enqueuePrint(self, data, msg):
        print('\tenqueue(%5s) - user: %2d, arrival : %2d, service_start : %2d, service_time: %2d' % (msg, data[0], data[1], data[2], data[-2]))

    def __dequeuePrint(self, data):
        print('\tdequeue - user: %2d, arrival : %2d, service_start : %2d, service_time: %2d' % (data[0], data[1], data[2], data[-2]))
 
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
        # join 함수 overriding. 권장하지는 않는다고 한다.
        threading.Thread.join(self)
        return self._return

def printResult(customer_data, windows):
# - 전체 통계 : 평균 큐 대기시간, 평균 서비스 시간, 전체 서비스 시간, 전체 고객 수
    def printAllStatistics(service_time_arr, wait_time_arr, customer_cnt):
        print('전체 통계')
        print('\t평균 큐 대기시간 : %3.2fmin, 평균 서비스 시간 : %3.2fmin'
            % (sum(wait_time_arr) / customer_cnt, sum(service_time_arr) / customer_cnt))
        print('\t전체 서비스 시간 : %3dmin' % sum(service_time_arr))

# - 개별 고객 : 도착시간, 시작시간, 대기시간, 서비스시간
    def printSepStatistics(customer_data):
        print('고객별 통계')
        for customer in customer_data:
            print('\t%3d | arrival : %3d, start : %3d, wait : %3dmin, service : %3dmin'
                % (customer[0], customer[1], customer[2], customer[-1], customer[-2]))

    # customer_data = [user idx, arrival time, service start time, service time, wait time]
    service_time_arr = [ x[-2] for x in customer_data ]
    wait_time_arr = [ x[-1] for x in customer_data ]
    customer_cnt = len(service_time_arr)
    print('창구 개수 : %2d, 운영 시간 : %3dmin' % (windows, MAX_TIME))
    printAllStatistics(service_time_arr, wait_time_arr, customer_cnt)
    printSepStatistics(customer_data)

def initSize():
    while True:
        windows = input("창구 개수 입력(1~5) >> ")
        try:
            if not windows.isdecimal():
                raise NotNumErr(windows)

            windows = int(windows)
            if windows < 1:
                raise NumRngErr(windows)
            if windows > 5:
                raise NumRngErr(windows)

        except NotNumErr as err:
            print(err)
            continue
        
        except NumRngErr as err:
            print(err)
            continue

        return windows

queue = Queue(QUEUE_SIZE) # taffy 상점의 대기열
customer_idx = 0
result = None
windows = initSize()  # taffy 상점의 창구 개수

queue_lock = threading.Lock()

runner = ThreadVariable(MAX_TIME)

for _ in range(windows):
    th = ConsumerThread()
    th.start()

mainThread = threading.current_thread()
for thread in threading.enumerate():
    if thread is not mainThread:
        result = thread.join()

printResult(result, windows)