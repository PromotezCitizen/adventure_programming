# 0 : Not alloc
# 1 : Alloced

from mem_alloc_class import Allocation

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
        free_space = mymem.myfree()
        try:
            allocation.remove(free_space)
        except:
            None
    return allocation

mymem = Allocation(0)
allocation = []

while True:
    allocation = switches(allocation, input("malloc, free, exit >> "))
    if allocation == "exit":
        break
    mymem.printStat()