import msvcrt

class Spin():
    def __init__(self):
        self.__pause = False
        None

    def spin(self):
        if msvcrt.kbhit():
            ch = msvcrt.getch()
            print(ch, type(ch))
            self.__pause = not self.__pause

    def isPause(self):
        return self.__pause


if __name__ == "__main__":
    spin = Spin()
    temp = 0
    while True:
        t = 0
        spin.spin()
        while spin.isPause():
            t += 1
            spin.spin()
            if t % 10000 == 0:
                print(t, 'sub while')
        temp += 1
        if temp % 10000 == 0:
            print(temp, 'main while')