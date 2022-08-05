class Huffman():
    def __init__(self, filename):
        self._filename = filename   # 읽을 파일 이름
        self._lines = None          # 읽은 파일의 전체 내용 저장
        self._head_tree = None      # 허프만 트리의 헤드 노드 저장 
        self._encoded_str = ""      # 인코딩된 문자열
        self._header_data = {}      # { key:data, value:code }
                                    # 허프만 부호화된 문자와 그에 해당하는 코드 저장

    def _getBinLines(self):
        with open(self._filename, 'rb') as f:
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