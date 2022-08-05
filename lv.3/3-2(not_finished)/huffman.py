class Huffman():
    def __init__(self, filename):
        self._lines = None
        self._head = None
        self._encoded_str = ""
        self._filename = filename

    def _getBinLines(self):
        with open(self._filename, 'rb') as f:
            self._lines = list(f.read())

    def _isInt(self, val):
        try:
            int(val)
        except:
            return False
        return True

    def printHuffmanTree(self):
        self._printHuffmanTree(self._head)

    def _printHuffmanTree(self, huffman):
        node = huffman.getLeft()
        if node is not None:
            self._printHuffmanTree(node)

        node = huffman.getRight()
        if node is not None:
            self._printHuffmanTree(node)

        data = huffman.getData()

        if self._isInt(data['data']):
            print(data)

    def printHuffmanTreeLMR(self):
        self._printHuffmanTreeLMR(self._head)

    def _printHuffmanTreeLMR(self, huffman):
        node = huffman.getLeft()
        if node is not None:
            self._printHuffmanTreeLMR(node)

        node = huffman.getRight()
        if node is not None:
            self._printHuffmanTreeLMR(node)

        data = huffman.getData()

        print(data)