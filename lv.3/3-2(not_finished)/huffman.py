from multipledispatch import dispatch

class Huffman():
    def __init__(self, data=None, cnt=None, code=None):
        self._data = data
        self._cnt = cnt
        self._code = code
        self._right = None
        self._left = None

    @dispatch()
    def setRight(self):
        self._right = Huffman()
    @dispatch(object)
    def setRight(self, huffman):
        self._right = huffman

    def getRight(self): # goRight
        return self._right

    @dispatch()
    def setLeft(self):
        self._left = Huffman()
    @dispatch(object)
    def setLeft(self, huffman):
        self._left = huffman
    
    def getLeft(self): # goLeft
        return self._left

    def print(self):
        print('data: {0}, cnt: {1}, code: {2}'.format(self._data, self._cnt, self._code))

    def setData(self, data, cnt, code):
        self._data = data
        self._cnt = cnt
        self._code = code

    def getData(self):
        return { 'data': self._data, 'cnt': self._cnt, 'code': self._code }

    def nodes(self):
        None

huffman = Huffman()
next = huffman
for _ in range(3):
    next.setLeft()
    next = next.getLeft()
next.setData('a', 10, '100010')

huffman.getLeft().getLeft().getLeft().print()

# 0x242


def getBinLines(filename):
    with open(filename, 'rb') as f:
        lines = f.readlines()
        lines = [ list(x) for x in lines ]
    return lines

def getBinDict(lines):
    data_dict = {}
    for line in lines:
        for data in line:
            try:
                data_dict[data] += 1
            except:
                data_dict[data] = 1

    return data_dict

def getHuffmanDict(data_dict):
    huffman_dict = {}
    for key, val in data_dict.items():
        huffman_dict[key] = Huffman(key, val)

    return huffman_dict

def isInt(val):
    ret_val = True
    try:
        int(val)
    except:
        ret_val = False
    return ret_val

def printDict(huffman, data=""):
    #print('left: {0}, right:{1}'.format(type(huffman.getLeft()), type(huffman.getRight())))
    node = huffman.getLeft()
    if node is not None:
        printDict(node, data+'0')

    node = huffman.getRight()
    if node is not None:
        printDict(node, data+'1')

    print_data = huffman.getData()

    if isInt(print_data['data']):
        print(print_data)


lines = getBinLines('test.txt')
data_dict = getBinDict(lines)
huffman_dict = getHuffmanDict(data_dict)


# data_dict = {}
# for line in lines:
#     for data in line:
#         try:
#             data_dict[data] += 1
#         except:
#             data_dict[data] = 1
# print(lines)

# huffman_dict = {}
# for key, val in data_dict.items():
#     data_dict[key] = Huffman(key, val)

temp_data = ''
temp_data_cnt = None

# for val in data_dict.values():
#     print(val.getData())
# print(len(data_dict))

while len(huffman_dict) > 1:
    # https://blockdmask.tistory.com/566 - dict sort
    huffman_dict = dict(sorted(huffman_dict.items(), key=lambda x: x[1].getData()['cnt'], reverse=True))

    temp_data += '-'

    huffman_right = huffman_dict.popitem()[1]
    data = huffman_right.getData()
    temp_cnt = data['cnt']
    #huffman_right = Huffman(data['data'], data['cnt'])

    huffman_left = huffman_dict.popitem()[1]
    data = huffman_left.getData()
    temp_cnt += data['cnt']
    #huffman_left = Huffman(data['data'], data['cnt'])

    huffman = Huffman(temp_data, temp_cnt)
    huffman.setRight(huffman_right)
    huffman.setLeft(huffman_left)

    huffman_dict[temp_data] = huffman

head = huffman_dict.popitem()[1]
# print(head.getLeft(), head.getRight())
printDict(head, '')





'''
# head = Huffman()

# temp_data += '-'

# huffman_right = Huffman()
# data = data_dict.popitem()
# temp_data_cnt = data[1]
# huffman_right.setData(data[0], data[1], None)

# huffman_left = Huffman()
# data = data_dict.popitem()
# temp_data_cnt += data[1]
# huffman_left.setData(data[0], data[1], None)

# head.setRight(huffman_right)
# head.setLeft(huffman_left)

# head.print()
# head.getRight().print()
# head.getLeft().print()

# temp_arr.append()
# data_dict[temp_data] = temp_data_cnt
'''