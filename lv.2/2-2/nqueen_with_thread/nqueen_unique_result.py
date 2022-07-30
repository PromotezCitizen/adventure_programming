import copy

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