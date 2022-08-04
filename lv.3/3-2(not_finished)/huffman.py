class Huffman():
    def __init__(self):
        self._data = None
        self._cnt = None
        self._code = None
        self._right = None
        self._left = None

    def setRight(self):
        self._right = Huffman()

    def getRight(self): # goRight
        return self._right

    def setLeft(self):
        self._left = Huffman()
    
    def getLeft(self): # goLeft
        return self._left

    def print(self):
        print('data: %s, cnt: %4d, code: %s' % (self._data, self._cnt, self._code))

    def setData(self, data, cnt, code):
        self._data = data
        self._cnt = cnt
        self._code = code

    def nodes(self):
        None

huffman = Huffman()
next = huffman
for _ in range(3):
    next.setLeft()
    next = next.getLeft()
next.setData('a', 10, '100010')

huffman.getLeft().getLeft().getLeft().print()

with open('test.txt') as f:
    None
