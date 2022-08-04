from encoding import HuffmanEncoding
# C:\\Users\\Han\\Documents\\now.png
# test.txt
encoding = HuffmanEncoding('test.txt') # encoding에서 허프만 트리는 필요없다. 
encoding.run()
#encoding.printHuffmanBin()
#encoding.printEncoded()

encoding.saveEncodedTree()
encoding.saveEncodedStr()

class HuffmanDecoding():
    def __init__(self, filename):
        self._filename = filename

    def run(self):
        None

with open('test.bin', 'rb') as f:
    bin = list(f.read())
    huffman_bin_len = bin.pop(0)
    print(huffman_bin_len)
    for idx in range(huffman_bin_len):
        data = bin.pop(0)
        code_len = bin.pop(0)
    print(bin)