class NumRngErr(Exception):
    def __init__(self, msg):
        self._msg = msg
    
    def __str__(self):
        return 'process number cant be negative, num: {0}'.format(self._msg)
        
def setSplitIdx(split_end, arr_left, arr_avg):
    split_start = split_end
    split_end += arr_avg
    if arr_left > 0:
        split_end += 1
        arr_left -= 1
    return split_start, split_end, arr_left

def dataSplit(arr, thread_num):
    try:
        if thread_num < 0:
            raise NumRngErr(str(thread_num))
        arr_left = len(arr) % thread_num
        arr_avg = len(arr) // thread_num
        split_start, split_end, arr_left = setSplitIdx(0, arr_left, arr_avg)
        temp = []
        for _ in range(thread_num):
            temp.append(arr[split_start:split_end])
            split_start, split_end, arr_left = setSplitIdx(split_end, arr_left, arr_avg)
    except NumRngErr as err:
        print(err)
        return [], False
    except ZeroDivisionError:
        print('cant divided by 0')
        return [], False
    return temp, True

def printResult(runners, num_process, map_size, result_data, main_time, num_roach):
    print('run: %3d' % runners)
    print('process num: %3d' % num_process)
    print('map size: %2d' % map_size)
    print('all run: %4.12f(roaches: %2d)' % (main_time, num_roach))

    for idx, data in enumerate(result_data):
        print('%3d\tmove: %5d, real move: %5d, runtime: %4.12f'
            % (
                idx,
                data['mv'],
                data['mv_real'],
                data['runtime']
            ))

    print('avg move: %5.5f, avg real move: %5.5f, avg runtime: %4.12fsec'
        % (
            sum([ x['mv'] for x in result_data])/runners,
            sum([ x['mv_real'] for x in result_data])/runners,
            sum([ x['runtime'] for x in result_data])/runners
        ))

    print('avg move direction\n\tup: %5.1f, left: %5.1f, down: %5.1f, right: %5.1f'
        % (
            sum([ x['direct'][0] for x in result_data])/runners,
            sum([ x['direct'][1] for x in result_data])/runners,
            sum([ x['direct'][2] for x in result_data])/runners,
            sum([ x['direct'][3] for x in result_data])/runners
        ))

    print('avg real move direction\n\tup: %5.1f, left: %5.1f, down: %5.1f, right: %5.1f'
        % (
            sum([ x['direct_real'][0] for x in result_data])/runners,
            sum([ x['direct_real'][1] for x in result_data])/runners,
            sum([ x['direct_real'][2] for x in result_data])/runners,
            sum([ x['direct_real'][3] for x in result_data])/runners
        ))