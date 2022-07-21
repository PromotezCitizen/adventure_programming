import random
import time

MAX_TIME = 480

class Queue():
    def __init__(self):
        self.__queue = [] # idx, service_time, arrval_time, wait_time
        self.__waiters = 0
        self.__queue_size = 5
        None

    def enqueue(self, data):
        self.__waiters += 1
        self.__queue.append(data)
    
    def dequeue(self):
        self.__waiters -= 1
        return self.__queue.pop(0)

    def insert(self, data):
        self.__waiters += 1
        self.__queue.insert(0, data)

    def print(self):
        print('\t', self.__queue)
    
    def isFull(self):
        return self.__waiters == self.__queue_size

    def isEmpty(self):
        return self.__waiters == 0

    def addWaitTimes(self):
        for customer in self.__queue:
            customer[-1] += 1

waiter_queue = Queue()
service_time_arr = []
service_time_left = 0
custom_idx = 1
turn = 1

# run
# 영업시간 직전에 받은 고객은 
while turn < 100:
    print('now turn : ', turn)
    turn += 1
    # time.sleep(1)
    
    if random.randint(1,4) == 4:
        print('\t pushed')
        if not waiter_queue.isFull():
            service_time = random.randint(1, 10)
            # init
            # customer_idx == idx, service_time == random
            # arival_turn == turn, wait_init == 0
            waiter_queue.enqueue([custom_idx, service_time, turn, 0])
            print('\tappend', custom_idx, service_time)
            custom_idx += 1

    if waiter_queue.isEmpty():
        continue

    if service_time_left == 0:
        temp = waiter_queue.dequeue()
        temp.insert(-1, turn) # service_start time
        service_time_left = temp[1]
        service_time_arr.append(temp)
        print("\tpop ", temp)
        print('\t', sum([x[1] for x in service_time_arr]), service_time_arr)
    else:
        waiter_queue.addWaitTimes()
        service_time_left -= 1
        

def printResult(waiter_queue, service_time_arr):
    waiter_queue.print()
    service_times = [x[1] for x in service_time_arr]
    wait_times = [x[-1] for x in service_time_arr]
    arrival_times = [x[-3] for x in service_time_arr]
    service_start = [x[-2] for x in service_time_arr]

    print('처리된 고객들')
    for idx, data in enumerate(service_times):
        print('\t%2d customer - arrival : %3d, start : %3d, service : %3d, wait : %3d'
            % (idx, arrival_times[idx], service_start[idx], service_times[idx], wait_times[idx]))

    print('전체 통계')
    print('\twait: %d, service: %d' % (sum(wait_times), sum(service_times)))
    print('\tavg service: %0.2f' % (sum(service_times) / len(service_times)))
    print('\tavg wait: %0.2f' % (sum(wait_times) / len(wait_times)))

# 큐 대기시간 - wait_time
# 평균 큐 대기시간 - wait_time / len(service_time)
# 전체 서비스 시간 - sum(service_times)
# 평균 서비스 시간 - sum(service_times) / len(service_times)
# 전체 고객 수 - len(service_times)

# service time queue : Custom No, service_time, arrval_time, start_time, wait_time

printResult(waiter_queue, service_time_arr)