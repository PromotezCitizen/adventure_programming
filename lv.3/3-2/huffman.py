# 파일 구조
#   magic number(2byte)
#   len of extension(1byte)
#   extensions(<len of extension>bytes)
#   len of huffman_code num
#   huffman code key-value
#    eg)[
#           data
#           len(8byte씩 나눔)
#           encoded_data
#       ]
#   power share remainder <- 인코딩된 문자열 길이 저장
#   encoded str

class Huffman():
    def __init__(self):
        self._lines = None          # 읽은 파일의 전체 내용 저장
        self._head_tree = None      # 허프만 트리의 헤드 노드 저장 
        self._encoded_str = ""      # 인코딩된 문자열
        self._header_data = {}      # { key:data, value:code }
                                    # 허프만 부호화된 문자와 그에 해당하는 코드 저장
        self._origin_ext = []       # 원본 파일 확장자

    def __enter__(self): # with문 사용시 필요
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        print(exc_type, exc_val, exc_tb)

    def _getBinLines(self, filename):
        with open(filename, 'rb') as f:
            self._lines = list(f.read())

    def _isInt(self, val):
        try:
            int(val)
        except:
            return False
        return True

    # tree의 print는 중위 순회로 구현

    def printHuffmanTree(self):
        self._printHuffmanTree(self._head_tree)

    def _printHuffmanTree(self, huffman):
        node = huffman.getLeft()
        if node is not None:
            self._printHuffmanTree(node)

        data = huffman.getData()
        if self._isInt(data['data']):
            print(data)

        node = huffman.getRight()
        if node is not None:
            self._printHuffmanTree(node)

    def printHuffmanTreeALL(self):
        self._printHuffmanTreeALL(self._head_tree)

    def _printHuffmanTreeALL(self, huffman):
        node = huffman.getLeft()
        if node is not None:
            self._printHuffmanTreeALL(node)

        data = huffman.getData()
        print(data)

        node = huffman.getRight()
        if node is not None:
            self._printHuffmanTreeALL(node)

    def printHuffmanKeyVal(self):
        for code, data in self._header_data.items():
            print("%s\t(%3d) - %-30s" % (chr(code), code, data))

# https://pydole.tistory.com/entry/Python-%EC%A0%95%EB%A0%AC%EA%B3%BC-%EA%B3%B5%EB%B0%B1%EC%9D%84-%EC%9D%B4%EC%9A%A9%ED%95%98%EC%97%AC-%EB%B3%B4%EA%B8%B0%EC%A2%8B%EA%B2%8C-%EC%B6%9C%EB%A0%A5%ED%95%98%EA%B8%B0
# 파이썬 문자열 우측정렬 출력