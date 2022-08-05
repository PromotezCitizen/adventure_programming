class NumRngErr(Exception): # 사용자 정의 에러
    def __init__(self, msg):
        self.msg = msg
    
    def __str__(self):
        return "[RNG error] input value : " + str(self.msg)

class NotNumErr(Exception):
    def __init__(self, msg):
        self.msg = msg
    
    def __str__(self):
        return "[NUM error] input value : " + str(self.msg)

class Allocation():

    def __init__(self):
        self.__alloc.append([0, self.__allocArr()])
        
        self.__alloc = []
        self.__alloc_dict = {}
        self.__alloc_flag = 0
        while True:
            try:
                self.__alloc_flag = input("1. first fit, 2. best fit, 3. worst fit >> ")
                if not self.__alloc_flag.isdigit():
                    raise NotNumErr(self.__alloc_flag)
                
                self.__alloc_flag = int(self.__alloc_flag)-1
                if self.__alloc_flag < 0:
                    raise NumRngErr(self.__alloc_flag)
                if self.__alloc_flag > 2:
                    raise NumRngErr(self.__alloc_flag)
                
            except NotNumErr as err:
                print(err)
                continue
            
            except NumRngErr as err:
                print(err)
                continue

            break
        
    
    def __allocArr(self):
        # arr size selection
        while True:
            arrsize = input("배열 크기 입력(10 이상) >> ")
            try:
                if not arrsize.isdigit():
                    raise NotNumErr(arrsize)
                arrsize = int(arrsize)
                if arrsize < 10:
                    raise NumRngErr(arrsize)
                break

            except NotNumErr as err:
                print(err)

            except NumRngErr as err:
                print(err)

        return arrsize

    def firstfit(self, mem_size):
        # mem data append
        for idx, data in enumerate(self.__alloc):
            if mem_size > data[1]:
                continue
            mem_start = self.__memAppend(idx, mem_size)
            break

        return mem_start

    def bestfit(self, mem_size):
        # select which memory use
        self.__alloc.sort(key=lambda x:x[0], reverse=True)
        self.__alloc.sort(key=lambda x:x[1], reverse=True)

        idx_temp = 0
        for idx ,data in enumerate(self.__alloc):
            if data[1] >= mem_size:
                idx_temp = idx
            else:
                break
        
        # mem data append
        mem_start = self.__memAppend(idx_temp, mem_size)
        return mem_start

    def worstfit(self, mem_size):
        # mem data append
        self.__alloc.sort(key=lambda x:x[1], reverse=True)

        mem_start = self.__memAppend(0, mem_size)
        return mem_start

    def __memAppend(self, idx, mem_size):
        # get memory alloc start location
        # append alloc start location and memory size to dictionary
        # modify array
        mem_start = self.__alloc[idx][0]
        self.__alloc_dict[mem_start] = mem_size
        self.__alloc[idx] = [ mem_start + mem_size, self.__alloc[idx][1] - mem_size ]
        return mem_start

    def myalloc(self):
        mem_size = int(input("메모리 크기 입력 >> "))
        # if not available in memory...
        # return error: -1
        if len(self.__alloc) == 0:
            return -1

        # if not fit mem size in memory...
        # return error: -1
        exit_flag = 0
        for _, data in enumerate(self.__alloc):
            if mem_size > data[1]:
                exit_flag += 1

        if exit_flag == len(self.__alloc):
            return -1

        # mem append method
        if self.__alloc_flag == 0: # fitst fit
            mem_start = self.firstfit(mem_size)
        elif self.__alloc_flag == 1: # best fit
            mem_start = self.bestfit(mem_size)
        elif self.__alloc_flag == 2: # worst fit
            mem_start = self.worstfit(mem_size)

        # delete mem
        while True:
            is_deleted = self.__del()
            if is_deleted == True:
                break

        return mem_start

    def __del(self):
        # delete mem data if left mem size === 0
        # True  : mem size === 0 block Not in mem data
        # False : mem size === 0 block in mem data
        for idx, data in enumerate(self.__alloc):
            if data[1] == 0:
                self.__alloc.pop(idx)
                return False
        return True

    def myfree(self):
        if len(self.__alloc_dict) == 0:
            print("Not available ADDRESS - all is free")
            return
        try:
            free_mem = int(input("free 주소 입력 >> "))
            self.__alloc.append([free_mem, self.__alloc_dict[free_mem]]) # append to mem left space
            self.__alloc.sort(key=lambda x:x[0])
            del self.__alloc_dict[free_mem] # usage mem delete
            while True:
                is_merged = self.__merge()
                if is_merged == True:
                    break
        except:
            print("Not available ADDRESS - memory exception")

        return free_mem
    
    def __merge(self):
        # if can merge memory free space, merge
        # e.g.) mem free space(aka. fs) >> [[0,10], [10,30]]
        #       a) fs[0][0](index:0 - mem start) + fs[0][1](index:0 - mem alloc size)
        #       b) fs[1][0](index:1 - mem start)
        #       if a) equals b) then merge.
        #           1. fs[0][1] << fs[0][1] + fs[1][1]
        #           2. delete fs[1]
        for idx, data in enumerate(self.__alloc[:-1]):
            if data[0] + data[1] == self.__alloc[idx+1][0]:
                self.__alloc[idx][1] += self.__alloc[idx+1][1]
                self.__alloc.pop(idx+1)
                return False
        return True

    def printStat(self):
        print("mem space : ", self.__alloc)
        print_str = "mem usage : "
        for k, v in sorted(self.__alloc_dict.items()):
            print_str += "[" + str(k) + ": " + str(v) + "] "
        print(print_str)
