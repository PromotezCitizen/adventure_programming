import random
from taffy_queue import Queue

MAX_TIME = 480
QUEUE_SIZE = 5

def printResult(waiter_queue, service_time_arr):
    # 큐 대기시간 - wait_time
    # 평균 큐 대기시간 - wait_time / len(service_time)
    # 전체 서비스 시간 - sum(service_times)
    # 평균 서비스 시간 - sum(service_times) / len(service_times)
    # 전체 고객 수 - len(service_times)

    print('남은 고객')
    waiter_queue.print()

    # service time queue : Custom No, service_time, arrval_time, start_time, wait_time
    service_times = [x[1] for x in service_time_arr]
    wait_times = [x[-1] for x in service_time_arr]
    arrival_times = [x[-3] for x in service_time_arr]
    service_start = [x[-2] for x in service_time_arr]

    print('처리된 고객들')
    for idx, _ in enumerate(service_times):
        print('\t%2d customer - arrival : %3d, start : %3d, service : %3d, wait : %3d'
            % (idx, arrival_times[idx], service_start[idx], service_times[idx], wait_times[idx]))

    print('전체 통계')
    print('\tcustomers : %d' % (len(service_times)))
    print('\twait: %d, service: %d' % (sum(wait_times), sum(service_times)))
    print('\tavg service: %0.2f' % (sum(service_times) / len(service_times)))
    print('\tavg wait: %0.2f' % (sum(wait_times) / len(wait_times)))

def run():
    waiter_queue = Queue(QUEUE_SIZE)
    service_time_arr = []
    service_time_left = 0
    custom_idx = 1
    turn = 1

    # run
    # 영업시간 직전까지 고객 처리. 이후에 큐에 있는 고객은 무시
    while turn <= MAX_TIME:
        turn += 1
        
        if random.randint(1,4) == 4:
            if not waiter_queue.isFull():
                print('now turn : ', turn)
                service_time = random.randint(1, 10)
                # init
                # customer_idx == idx, service_time == random
                # arival_turn == turn, wait_init == 0
                waiter_queue.enqueue([custom_idx, service_time, turn, 0])
                print('\t%2d customer append(time:%3d)' % (custom_idx, turn))
                waiter_queue.print()
                custom_idx += 1

        if waiter_queue.isEmpty():
            continue

        if service_time_left == 0:
            print('now turn : ', turn)
            temp = waiter_queue.dequeue()
            temp.insert(-1, turn) # service_start time
            service_time_left = temp[1]
            service_time_arr.append(temp)
            print("\tqueue removed :: customer %2d, arrival %3d, start %3d, wait %2d, service %2d"
                % (temp[0], temp[2], temp[3], temp[4], temp[1]))
        else:
            waiter_queue.addWaitTimes()
            service_time_left -= 1
    
    print('\n')
    return waiter_queue, service_time_arr

waiters, service = run()
printResult(waiters, service)