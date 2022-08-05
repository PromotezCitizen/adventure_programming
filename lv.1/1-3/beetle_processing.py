import time
import multiprocessing as mp
from beetle import Beetle

def useProcessing(map_size, splited, num_roach):
    return_dict = mp.Manager().dict()
    jobs = []

    start = time.perf_counter()
    for idx, calc_range in enumerate(splited):
        p = mp.Process(target=worker, args=(idx, map_size, calc_range, return_dict, num_roach))
        jobs.append(p)
        p.start()
    
    for p in jobs:
        p.join()

    beetle_result_list = []
    for x in return_dict.values():
        for y in x:
            beetle_result_list.append(y)
    end = time.perf_counter()
    return beetle_result_list, end-start

def worker(idx, map_size, calc_range, return_dict, num_roach):
    beetle = Beetle(map_size, calc_range, num_roach)
    nqueen_result = beetle.start()
    return_dict[idx] = nqueen_result