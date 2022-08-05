from huffman import Huffman

class HuffmanDecoding():
    def __init__(self, filename):
        self._filename = filename
        self._head_data = []
        self._encoded_data = []
        self._head = None
        self._encoded_str = None
        self._result = []

        self._huffman_code_bin = {}

    def run(self):
        self._getDecodedData(self._filename)
        self._getDecodeInfoFromBin()
        self._makeHuffmanTree()
        self._getEncodedStr()
        self._decodeStr()

    def _getDecodedData(self, filename):
        with open(filename, 'rb') as f:
            self._encoded_data = list(f.read())

    def _getDecodeInfoFromBin(self):
        huffman_bin_len = self._encoded_data.pop(0)
        for _ in range(huffman_bin_len):
            data = self._encoded_data.pop(0)
            code_len = self._encoded_data.pop(0)
            code = ""
            max_range = (code_len+7) // 8
            for idx in range(max_range):
                temp = bin(self._encoded_data.pop(0))[2:]
                filler = 8 if idx < max_range - 1 else code_len
                # https://www.delftstack.com/ko/howto/python/pad-string-with-zeros-in-python/
                code += temp.zfill(filler) # 원하는 길이가 될때까지 좌측에 추가

                # print("bin:%8s, bin_len:%2d, code_len:%2d, start_idx:%2d, now_idx:%d, fill_pos:%2d" % 
                #    (temp, len(temp), code_len, 8*idx, idx, filler))
                code_len -= 8
            # print(data, code_len, code)
            # print('')
            self._head_data.append({'data': data, 'code_len': len(code), 'code': code})
            self._huffman_code_bin[data] = code


    def test(self):
        print(self._head.getLeft().getLeft().getLeft().getLeft().getRight().getLeft())
        print(self._head.getLeft().getLeft().getLeft().getLeft().getRight().getData())

    def _makeHuffmanTree(self):
        self._head = Huffman()

        for data in self._head_data: # header_data : { data, code }
            temp = self._head
            for idx in data['code']:
                if idx == '0': # left
                    if temp.getLeft() is None:
                        temp.setLeft()
                        temp.setData('-', -1, '')
                    temp = temp.getLeft()
                else: # right
                    if temp.getRight() is None:
                        temp.setRight()
                        temp.setData('-', -1, '')
                    temp = temp.getRight()
            temp.setData(data['data'], data['code_len'], data['code'])

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

        if data['cnt'] > 0:
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

    def _getEncodedStr(self):
        power = self._encoded_data.pop(0)
        share = self._encoded_data.pop(0)
        remainder = self._encoded_data.pop(0)

        # print(power, share, remainder)

        str_len = (0 if power == 0 else 256**power + 256*share + remainder)
        self._encoded_str = ""
        for _ in range(str_len//8):
            self._encoded_str += bin(self._encoded_data.pop(0))[2:].zfill(8)
        if str_len % 8 != 0:
            self._encoded_str += bin(self._encoded_data.pop(0))[2:].zfill(str_len % 8)


    def _decodeStr(self):
        temp = self._head
        result_str = ""
        max_len = len(self._encoded_str)
        print(self._encoded_str)
        for idx, data in enumerate(self._encoded_str):
            if data == '0':
                if temp.getLeft() is None:
                    print(chr(temp.getData()['data']), result_str)
                    self._result.append(temp.getData()['data'])
                    if idx != max_len: temp = self._head.getLeft()
                    result_str = ""
                else:
                    temp = temp.getLeft()

            else:
                if temp.getRight() is None:
                    print(chr(temp.getData()['data']), result_str)
                    self._result.append(temp.getData()['data'])
                    if idx != max_len: temp = self._head.getRight()
                    result_str = ""
                else:
                    temp = temp.getRight()
            result_str += data
            print(data, end="")
        self._result.append(temp.getData()['data'])

    def save(self, filename):
        with open(filename, 'wb') as f:
            for data in self._result:
                f.write(bytes([data]))