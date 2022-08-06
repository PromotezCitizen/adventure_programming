# # ========== int를 바이트 타입으로 저장 ===============
# # data = 200
# # with open('test.bin', 'wb') as f:
# #     f.write(bytes([data]))
# # ===================================================

# # ========= 문자열을 균일한 사이즈로 분할 =============
# def spliter(arr, size):
#     ret = []
#     for idx in range(0, len(arr), size):
#         ret.append(arr[idx:idx+size])
#     return ret
# encoded = "1110100110000101001011100111000001010110100000001100101001000000001000001000110100000"

# for arr in spliter(encoded, 8):
#     print(int(arr, 2))
# # ===================================================

# # ========= 파일에서 데이터를 읽어와 리스트로 =========
# # ============== 2차원 배열 이용 =====================
# with open('asdf.txt', 'rb') as f:
#     lines = f.readlines()
#     lines = [ list(x) for x in lines ]

#     print(lines)

# for line in lines:
#     for data in line:
#         print(data)
# # ===================================================

# # =========== 1차로 만든 문자열 길이 확인 =============
# temp = 2602

# power = 0
# while 256**power < temp:
#     power += 1
# power -= 1
# temp -= 256**power
# share = temp // 256
# remainder = temp % 256

# with open('asdf.bin', 'wb') as f:
#     print(power, share, remainder)
#     f.write(bytes([power]))
#     f.write(bytes([share]))
#     f.write(bytes([remainder]))

# with open('asdf.bin', 'rb') as f:
#     temp = f.read()
#     for data in temp:
#         print(type(data))
#         print(bin(data)[2:])
# # ===================================================


# # ========= 바이너리 데이터를 문자로 바꿔보자===========
# with open('test.bin', 'rb') as f:
#     data = f.read(1)

# print(type(data), data)
# print(type(ord(data)), ord(data))
# print(type(chr(ord(data))), chr(ord(data)))
# # ===================================================

# # ========= 빈 배열도 join을 쓸 수 있을까? ============
# temp = []
# print(len(temp))
# print(''.join(temp), len(''.join(temp)))
# # ===================================================

# # # =========== 2차로 만든 문자열 길이 확인 =============

# str_len = 1044728937592
# origin = str_len

# # ============ encoder - saveEncodeStrLen =============
# # =====================================================
# str_len_arr = []
# str_len = str_len

# max_power = 0
# while 256**max_power < str_len:
#     max_power += 1
# max_power -= 1

# with open('test.bin', 'wb') as f:
#     f.write(bytes([max_power+1])) # range에서는 실제 길이보다 1 짧다
#     for i in range(max_power):
#         f.write(bytes([str_len // 256**(max_power - i)]))
#         str_len_arr.append(str_len // 256**(max_power - i))
#         # f.write(bytes([str_len_arr[-1]]))
#         str_len -= 256**(max_power-i) * str_len_arr[-1]
#     f.write(bytes([str_len % 256]))
#     str_len_arr.append(str_len % 256)
#     # f.write(bytes([str_len_arr[-1]]))
# print(str_len_arr) # 실제 코드에서는 테스트 용도로만 사용
# # =====================================================


# # ============== decoder - getDecodeInfo ==============
# # =====================================================
# with open('test.bin', 'rb') as f: # 실제는 self._lines로 쓴다
#     str_arr_len = ord(f.read(1))
#     print(str_arr_len)
#     str_len_arr = list(f.read(str_arr_len))

# print(str_len_arr)

# adder = 0
# for i, data in enumerate(str_len_arr):
#     adder += 256**(str_arr_len-1 - i) * data
# print(adder == origin, adder, origin) # 실제 코드에서는 테스트 용도로만 사용

# # # str_len = f.read(1) # 문자열 길이 저장한 배열 크기. 256**power에서도 쓴다.
# # # str_len_arr = line(f.read(str_len))
# # str_arr_len = len(str_len_arr) # 실제 코드에서는 사용하지 않을 예정
# # adder = 0
# # for i, data in enumerate(str_len_arr):
# #     adder += 256**(str_arr_len-1 - i) * data
# # print(adder == origin, adder, origin) # 실제 코드에서는 테스트 용도로만 사용
# # =====================================================

# # # ===================================================

# =================== 문자열 나누기 test ===================
def spliter(arr, arr_len):
    temp = []
    each_str_len = len(arr) // arr_len
    remainder_str_len = len(arr) % arr_len
    last = -1
    print(each_str_len, remainder_str_len, len(arr))
    for idx in range(arr_len): 
        # 0              ~ each_str_len -1
        # 1*each_str_len ~ 2*each_str_len - 1
        # 2*each_str_len ~ 3*each_str_len - 1
        # 3*each_str_len ~
        idx_adder = 1 if remainder_str_len > 0 else 0
        remainder_str_len -= 1
        start = last+1
        last = (start-1) + each_str_len + idx_adder
        print(start, last, last-start+1)

        temp.append(arr[start:last+1])

    return temp

# str_arr = "ㄱㄴㄷㄻㅄㅇㅈㅊㅋㅌㅍㅎㅂㅂ"
# splited = spliter(str_arr, 4)
# print(splited, [ len(x) for x in splited ])
# =========================================================

# ================= multiprocessing =====================
# ===== __name__ == "__main__" 없이 사용할 수 있을까? =====
import multiprocessing

def worker(procnum, return_dict, calc_range):
    """worker function"""
    print(str(procnum) + " represent!")
    temp = []
    for data in calc_range:
        temp.append(data)
    return_dict[procnum] = temp
    print(return_dict[procnum], len(return_dict[procnum]))
    # return_dict[procnum] = [] -> return_dict[procnum].append()는 되지 않는다


def main():
    print('proc: ', multiprocessing.current_process().name)
    if multiprocessing.current_process().name == "MainProcess":
        process_num = 4
        multiprocessing.freeze_support()
        manager = multiprocessing.Manager()
        return_dict = manager.dict()
        jobs = []
        arg = "MainProcess"
        data = spliter(arg, process_num)
        for i in range(process_num):
            p = multiprocessing.Process(target=worker, args=(i, return_dict, data[i]))
            jobs.append(p)
            p.start()

        for proc in jobs:
            proc.join()
        print(return_dict.items())

# main()
# =========================================================