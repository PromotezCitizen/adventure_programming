class Queue():
    def __init__(self, size):
        self.__max_size = size
        self.__queue = []

    def enqueue(self, data):
        self.__queue.append(data)
    
    def dequeue(self):
        return self.__queue.pop(0)

    def addWaitTime(self):
        for data in self.__queue:
            data[-1] += 1

    def isFull(self):
        return len(self.__queue) == self.__max_size

    def isEmpty(self):
        return len(self.__queue) == 0

    def print(self):
        print('\t\t', self.__queue)