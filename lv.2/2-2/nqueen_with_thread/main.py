from enum import unique
from nqueen_thread import NQueenThread
from nqueen import NQueen
import threading
import multiprocessing as mp
import copy

def data_split(arr, thread_num):
    def _set_split_idx(split_end, arr_left, arr_avg):
        split_start = split_end
        split_end += arr_avg
        if arr_left > 0:
            split_end += 1
            arr_left -= 1
        
        return split_start, split_end, arr_left

    try:
        arr_left = len(arr) % thread_num
        arr_avg = len(arr) // thread_num
        split_start, split_end, arr_left = _set_split_idx(0, arr_left, arr_avg)
        temp = []
        for _ in range(thread_num):
            temp.append(arr[split_start:split_end])
            split_start, split_end, arr_left = _set_split_idx(split_end, arr_left, arr_avg)
    except:
        print('cant divided by 0')
    return temp


def useThread(map_size, splited):
    for _, arr in enumerate(splited):
        nqueen_thread = NQueenThread(map_size, arr)
        nqueen_thread.run()

    nqueen_result_list = []
    nqueen_unique_result_list = []
    mainThread = threading.current_thread()

    for thread in threading.enumerate():
        if thread is not mainThread:
            nqueen_result, nqueen_unique_list = thread.join()
            nqueen_result_list.append(nqueen_result)
            nqueen_unique_result_list.append(nqueen_unique_list)

    for idx, list in nqueen_result_list:
        None

def worker(idx, map_size, calc_range, return_dict):
    nqueen = NQueen(map_size, calc_range)
    print('process %2d start' % idx)
    nqueen_result = nqueen.run()
    print('process %2d end' % idx)
    return_dict[idx] = nqueen_result

def getUniqueSolve(results):
    print('remove spin/reflect duplicate start')

    unique_results = copy.deepcopy(results)
    idx = 0
    for arr in unique_results:
        print('\t%6d/%6d' % (idx, len(unique_results)))
        isTrun2RightIn(unique_results, arr)
        isReflectiveIn(unique_results, arr)
        idx += 1

    print('remove spin/reflect duplicate end')
    return unique_results

def isTrun2RightIn(unique_results, target_arr):
    #data = copy.deepcopy(target_arr)
    size = len(target_arr)
    for _ in range(3):
        #data = [ list(reversed([x[col] for x in data])) for col in range(size) ]
        data = [ list(reversed([x[col] for x in target_arr])) for col in range(size) ]
        try:
            unique_results.remove(data)
        except:
            None

def isReflectiveIn(unique_results, target_arr):
    # data = copy.deepcopy(target_arr)
    # data = [ list(reversed(x)) for x in data ]
    data = [ list(reversed(x)) for x in target_arr ]
    size = len(target_arr)
    for _ in range(4):
        data = [ list(reversed([x[col] for x in data])) for col in range(size) ]
        try:
            unique_results.remove(data)
        except:
            None

def printFlag(arr, msg):
    if len(arr) == 0:
        print("결과 없음")
    else:
        print('case : %s' % msg)
        for idx, chess_map in enumerate(arr):
            printChessMap(idx, chess_map)

def printChessMap(idx, chess_map):
    print('result %3d' % idx)
    for x in chess_map:
        for data in x:
            print('%2d' % data, end=" ")
        print('')
    print('')

def useProcessing(map_size, splited):
    manager = mp.Manager()
    return_dict = manager.dict()
    jobs = []

    print('processing work start')
    for idx, calc_range in enumerate(splited):
        p = mp.Process(target=worker, args=(idx, map_size, calc_range, return_dict))
        jobs.append(p)
        p.start()

    for p in jobs:
        p.join()
    print('processing work end')

    results = []
    for x in return_dict.values():
        for y in x:
            results.append(y)
    unique_results = getUniqueSolve(results)

    # printFlag(results, 'result')
    # printFlag(unique_results, 'unique_result')

    print('results: %6d, unique results: %6d' % (len(results), len(unique_results)))


thread_num = 6
map_size = 12
splited = data_split([ x for x in range(map_size) ], thread_num)

# useThread(map_size, splited)

if __name__ == "__main__":
    useProcessing(map_size, splited)

    # data = [[0, 1, 0, 0, 0], [0, 0, 0, 1, 0], [1, 0, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 0, 1]]
    # printChessMap(-1, data)
    # data = [ list(reversed([x[col] for x in data])) for col in range(len(data)) ]
    # printChessMap(-1, data)
    # data  = isReflectiveIn(None, data)
    # printChessMap(-1, data)
    # data = [ list(reversed([x[col] for x in data])) for col in range(len(data)) ]
    # printChessMap(-1, data)

# https://www.inflearn.com/questions/85857 - multi processing
# https://www.delftstack.com/ko/howto/python/python-multiprocessing-vs-threading/ - 스레딩 vs 프로세싱