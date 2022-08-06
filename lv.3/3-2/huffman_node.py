from multipledispatch import dispatch

class HuffmanNode():
    def __init__(self, data=None, cnt=None, code=None):
        self._data = data
        self._cnt = cnt
        self._code = code
        self._right = None
        self._left = None

    @dispatch()
    def setRight(self):
        self._right = HuffmanNode()
    @dispatch(object)
    def setRight(self, huffman):
        self._right = huffman

    def getRight(self): # goRight
        return self._right

    @dispatch()
    def setLeft(self):
        self._left = HuffmanNode()
    @dispatch(object)
    def setLeft(self, huffman):
        self._left = huffman
    
    def getLeft(self): # goLeft
        return self._left

    def setData(self, data, cnt, code):
        self._data = data
        self._cnt = cnt
        self._code = code

    def getData(self):
        return { 'data': self._data, 'cnt': self._cnt, 'code': self._code }

    def print(self):
        print('data: {0}, cnt: {1}, code: {2}'.format(self._data, self._cnt, self._code))


# https://www.delftstack.com/ko/howto/python/how-to-convert-int-to-bytes-in-python-2-and-python-3/
# int to byte type

# https://www.daleseo.com/python-int-bases/
# 2진수 문자열 -> 10진수 숫자 변환

# https://www.delftstack.com/ko/howto/python/python-function-overloading/
# 파이썬은 기본적으로 오버로딩 지원 X -> dispatch 패키지를 통해 오버로딩 유사하게 나타냄