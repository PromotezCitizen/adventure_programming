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

        exit_flag = 0

        for idx, data in enumerate(self.__alloc):
            if mem_size > data[1]:
                exit_flag += 1
            
        if exit_flag == len(self.__alloc):
            return -1

        # mem data append
        for idx, data in enumerate(self.__alloc):
            if mem_size > data[1]:
                continue
            mem_start = data[0]
            self.__alloc_dict[mem_start] = mem_size
            self.__alloc[idx] = [ mem_start + mem_size, data[1] - mem_size ]
            break

        while True:
            is_deleted = self.__del()
            if is_deleted == True:
                break
    
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
            self.__alloc.sort(key=lambda x:x[0])
            del self.__alloc_dict[start]
            while True:
                is_merged = self.__merge()
                if is_merged == True:
                    break
        except:
            print("Not available ADDRESS - memory exception")
    
    def __merge(self):
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

def switches(allocation, switch):
    if switch.lower() == "exit":
        return "exit"
    if switch.lower() == "malloc":
        mem_start = mymem.myalloc()
        if mem_start == -1:
            print("Not available ADDRESS - malloc")
        else:
            allocation.append(mem_start)
    if switch.lower() == "free":
        free_space = int(input("free 주소 입력 >> "))
        mymem.myfree(free_space)
        try:
            allocation.remove(free_space)
        except:
            None
    return allocation

# 0 : first
# 1 : best
# 2 : worst

mymem = Allocation(0)
allocation = []

while True:
    allocation = switches(allocation, input("malloc, free, exit >> "))
    if allocation == "exit":
        break
    mymem.printStat()