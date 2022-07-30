from nqueen import NQueen
import multiprocessing as mp
import time


def useProcessing(map_size, splited):
    manager = mp.Manager()
    return_dict = manager.dict()
    jobs = []

    start_time = time.perf_counter()
    for idx, calc_range in enumerate(splited):
        p = mp.Process(target=worker, args=(idx, map_size, calc_range, return_dict))
        jobs.append(p)
        p.start()
    
    for p in jobs:
        p.join()

    nqueen_result_list = []
    for x in return_dict.values():
        for y in x:
            nqueen_result_list.append(y)

    #unique_results = getUniqueSolve(results)

    # printFlag(results, 'result')
    # printFlag(unique_results, 'unique_result')
    print(f"time elapsed : {int(round((time.perf_counter() - start_time) * 1000))}ms")
    print('results: %6d' % (len(nqueen_result_list)))
    # print('results: %6d, unique results: %6d' % (len(results), len(unique_results)))

def worker(idx, map_size, calc_range, return_dict):
    nqueen = NQueen(map_size, calc_range)
    nqueen_result = nqueen.run()
    return_dict[idx] = nqueen_result