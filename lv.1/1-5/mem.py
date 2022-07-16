# 0 : Not alloc
# 1 : Alloced

class NumRngErr(Exception): # 사용자 정의 에러
    pass

class NotNumErr(Exception):
    pass

class Allocation():
    __mem = []
    def __init__(self):
        self.__mem = [ 0 for _ in range(self.__allocArr())]
        print(self.__mem, len(self.__mem))
        None
    
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


    def myalloc():
        None

    def myfree():
        None


mymem = Allocation()