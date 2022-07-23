class Queue():
    def __init__(self, queue_size):
        self.__queue = [] # idx, service_time, arrval_time, wait_time
        self.__waiters = 0
        self.__queue_size = queue_size

    def enqueue(self, data):
        self.__waiters += 1
        self.__queue.append(data)
    
    def dequeue(self):
        self.__waiters -= 1
        return self.__queue.pop(0)

    def insert(self, data):
        self.__waiters += 1
        self.__queue.insert(0, data)

    def print(self):
        print('\t', self.__queue)
    
    def isFull(self):
        return self.__waiters == self.__queue_size

    def isEmpty(self):
        return self.__waiters == 0

    def addWaitTimes(self):
        for customer in self.__queue:
            customer[-1] += 1