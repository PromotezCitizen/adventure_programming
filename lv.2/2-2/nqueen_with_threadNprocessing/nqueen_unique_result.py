import copy

def getUniqueSolve(results):
    unique_results = copy.deepcopy(results)
    if len(unique_results) > 1:
        for arr in unique_results:
            isTrun2RightIn(unique_results, arr)
        for arr in unique_results:
            isReflectiveIn(unique_results, arr)

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
    size = len(data)
    for _ in range(4):
        data = [ list(reversed([x[col] for x in data])) for col in range(size) ]
        try:
            unique_results.remove(data)
        except:
            None