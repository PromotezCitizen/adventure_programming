from encoding import HuffmanEncoding
from decoding import HuffmanDecoding

# C:\\Users\\Han\\Documents\\now.png
# test.txt
encoding = HuffmanEncoding('test.txt') # encoding에서 허프만 트리는 필요없다. 
encoding.encode()
# encoding.printHuffmanTree()
encoding.save('test.bin')

print('')

decoding = HuffmanDecoding('test.bin')
decoding.decode()
# decoding.printHuffmanTree()
decoding.save('qwer.txt')

