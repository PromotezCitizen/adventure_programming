from codec import HuffmanCodec
import os
# C:\\Users\\Han\\Documents\\now.png
# test.txt

# cli를 사용하는 버전

codec = HuffmanCodec()

if __name__ == "__main__":
    codec.run()
    codec.save()
    os.system('pause')  


'''
# 코덱 만들기 전 사용했던 코드
        # encoder = HuffmanEncoder() # encoder에서 허프만 트리는 필요없다. 
        # encoder.encode()
        # # encoder.printHuffmanKeyVal()
        # # encoder.printHuffmanTree()
        # # encoder.printHuffmanTreeALL()
        # encoder.save()

        # print('='*30)

        # decoder = HuffmanDecoder()
        # decoder.decode()
        # # encoder.printHuffmanKeyVal()
        # # decoder.printHuffmanTree()
        # # decoder.printHuffmanTreeALL()
        # decoder.save()
'''

