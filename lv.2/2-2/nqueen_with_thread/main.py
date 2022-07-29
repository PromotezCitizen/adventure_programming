from nqueen_thread import NQueenThread
from nqueen import NQueen
import threading

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

thread_num = 8
map_size = 7
splited = data_split([ x for x in range(map_size) ], thread_num)

# nqueen = NQueen(map_size, [ x for x in range(map_size) ])
# print(nqueen.run())

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