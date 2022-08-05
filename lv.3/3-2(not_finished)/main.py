from encoder import HuffmanEncoder
from decoder import HuffmanDecoder

# C:\\Users\\Han\\Documents\\now.png
# test.txt

encoder = HuffmanEncoder() # encoder에서 허프만 트리는 필요없다. 
encoder.encode()
# encoder.printHuffmanKeyVal()
# encoder.printHuffmanTree()
# encoder.printHuffmanTreeALL()
encoder.save()

print('='*30)

decoder = HuffmanDecoder()
decoder.decode()
# encoder.printHuffmanKeyVal()
# decoder.printHuffmanTree()
# decoder.printHuffmanTreeALL()
decoder.save()