from nqueen_threading import useThreading
from nqueen_processing import useProcessing
from nqueen_unique_result import getUniqueSolve
import threading # 현재 thread가 main thread인지 확인

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

if __name__ == "__main__":
    if threading.currentThread() == threading.main_thread():
        thread_num = 6
        map_size = 10
        splited = data_split([ x for x in range(map_size) ], thread_num)

        print('process result')
        temp = useProcessing(map_size, splited)
        print(len(getUniqueSolve(temp)))
        # 멀티프로세스를 사용시 고유한 결과가 제대로 계산되지 않음
        print('=======================================')
        print('thread result')
        temp = useThreading(map_size, splited)
        print(len(getUniqueSolve(temp)))

# https://coding-groot.tistory.com/103 - threading
# https://www.inflearn.com/questions/85857 - multi processing
# https://www.delftstack.com/ko/howto/python/python-multiprocessing-vs-threading/ - 스레딩 vs 프로세싱