from encoding import HuffmanEncoding
from decoding import HuffmanDecoding

# C:\\Users\\Han\\Documents\\now.png
# test.txt
encoding = HuffmanEncoding('test.txt') # encoding에서 허프만 트리는 필요없다. 
encoding.run()
#encoding.printHuffmanBin()
#encoding.printEncoded()
encoding.save()


decoding = HuffmanDecoding('test.bin')
decoding.run()
# decoding.printHuffmanTree()
decoding.write()

