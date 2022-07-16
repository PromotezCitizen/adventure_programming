# 0 : Not alloc
# 1 : Alloced

class NumRngErr(Exception): # 사용자 정의 에러
    pass

class NotNumErr(Exception):
    pass

class Allocation():
    __mem_size = 0
    __alloc = []
    __alloc_dict = {}
    __alloc_flag = 0

    def __init__(self, alloc_flag):
        self.__mem_size= self.__allocArr()
        self.__alloc_flag = alloc_flag
        self.__alloc.append([0, self.__mem_size])
    
    def __allocArr(self):
        while True:
            arrsize = input("배열 크기 입력 >> ")
            try:
                if not arrsize.isdigit():
                    raise NotNumErr
                arrsize = int(arrsize)
                if arrsize < 10:
                    raise NumRngErr
                break

            except NotNumErr:
                print("숫자를 입력해주세요.", sep=" ")

            except NumRngErr:
                print("10 이상을 입력해주세요. ", sep=" ")

        return arrsize

    def myalloc(self):
        mem_size = int(input("메모리 크기 입력 >> "))
        if len(self.__alloc) == 0:
            return -1
        if mem_size > self.__alloc[0][1]:
            return -1

        for idx, data in enumerate(self.__alloc):
            mem_start = data[0]
            self.__alloc_dict[mem_start] = mem_size
            self.__alloc[idx] = [ mem_start + mem_size, data[1] - mem_size ]
            None

        while not self.__del():
            None
    
        return mem_start

    def __del(self):
        for idx, data in enumerate(self.__alloc):
            if data[1] == 0:
                self.__alloc.pop(idx)
                return False
        return True

    def myfree(self, start):
        try:
            self.__alloc.append([start, self.__alloc_dict[start]])
            del self.__alloc_dict[start]
            while not self.__merge():
                None
            self.__alloc.sort(key=lambda x:x[0])
        except:
            print("Not available ADDRESS")
    
    def __merge(self):
        for idx, data in enumerate(self.__alloc[:-2]):
            if data[0] + data[1] == self.__alloc[idx+1][0]:
                data[1] += self.__alloc[idx+1][1]
                self.__alloc.pop(idx+1)
                return False
        return True

    def printStat(self):
        print(self.__alloc)
        print(self.__alloc_dict)

# 0 : first
# 1 : best
# 2 : worst
allocation = []

mymem = Allocation(0)

mem_start = mymem.myalloc()
if mem_start != -1: allocation.append(mem_start)

mem_start = mymem.myalloc()
if mem_start != -1: allocation.append(mem_start)

mem_start = mymem.myalloc()
if mem_start != -1: allocation.append(mem_start)

print(allocation)

mymem.myfree(int(input("free 주소 입력 >> ")))
mymem.myfree(int(input("free 주소 입력 >> ")))
mymem.printStat()