class UCodeInterpreter():
    def __init__(self, folder, file):
        self.__folder_path = folder
        self.__file_path = file
        self.__proc_starts = None
        self.__label_starts = None

    def run(self):
        ucode = self._getUCODEData()
        self.__proc_starts = self._getStartPosition(ucode, 'proc')
        self.__label_starts = self._getStartPosition(ucode, 'nop')
        print(self.__proc_starts, self.__label_starts)
        return None

    def _getUCODEData(self):
        # folder_path = '레벨3.3 UCode테스트/'
        # file_path = 'test1.uco'

        # https://wikidocs.net/26 - readlines
        with open(self.__folder_path+self.__file_path, 'r') as f:
            raw_lines = f.readlines()

        trimed_lines = self._getTrimedStrList(raw_lines)
        converted_lines = self._getFormatedList(trimed_lines)
        return converted_lines

    def _getTrimedStrList(self, raw_lines):
        trimed_lines = []
        for line in raw_lines:
            # https://velog.io/@xdfc1745/Mote-python-%EC%8A%A4%ED%8A%B8%EB%A7%81-trim - str trim
            trimed_lines.append([ x for x in line.rstrip().split(' ') if x is not ''])
        return trimed_lines

    def _getFormatedList(self, trimed_lines):
        converted_lines = []
        for line in trimed_lines:
            if len(line) > 0:
                temp = self._getStringedInt2Int(line)
                converted_lines.append(temp)
        return converted_lines

    def _getStringedInt2Int(self, line):
        temp = []
        for data in line:
            try: data = int(data)
            except: None
            finally: temp.append(data)
        return temp

    def _getStartPosition(self, ucode, name):
        func_start = {}
        for idx, line in enumerate(ucode):
            if name in line: 
                # 우리가 찾는 것은
                #   [ <labe_name>, <'proc'/'nop'>, ... ]
                # 형식으로 되어있음
                func_start[line[0]] = idx
        return func_start


# interpreter = UCodeInterpreter('레벨3.3 UCode테스트/', 'test1.uco')
# interpreter.run()




















def getUCODEData():
    folder_path = '레벨3.3 UCode테스트/'
    file_path = 'test1.uco'

    # https://wikidocs.net/26 - readlines
    with open(folder_path+file_path, 'r') as f:
        raw_lines = f.readlines()

    trimed_lines = getTrimedStrList(raw_lines)
    converted_lines = getFormatedList(trimed_lines)
    return converted_lines

def getTrimedStrList(raw_lines):
    trimed_lines = []
    for line in raw_lines:
        # https://velog.io/@xdfc1745/Mote-python-%EC%8A%A4%ED%8A%B8%EB%A7%81-trim - str trim
        trimed_lines.append([ x for x in line.rstrip().split(' ') if x is not ''])
    return trimed_lines

def getFormatedList(trimed_lines):
    converted_lines = []
    for line in trimed_lines:
        if len(line) > 0:
            temp = getStringedInt2Int(line)
            converted_lines.append(temp)
    return converted_lines

def getStringedInt2Int(line):
    temp = []
    for data in line:
        try: data = int(data)
        except: None
        finally: temp.append(data)
    return temp

def getStartPosition(ucode, name):
    func_start = {}
    for idx, line in enumerate(ucode):
        if name in line: 
            # 우리가 찾는 것은
            #   [ <labe_name>, <'proc'/'nop'>, ... ]
            # 형식으로 되어있음
            func_start[line[0]] = idx
    return func_start

ucode = getUCODEData()
proc_starts = getStartPosition(ucode, 'proc')
label_starts = getStartPosition(ucode, 'nop')

turn = 0
idx = 0
ret_pos = None
while turn < 200:
    try:
        data = ucode[idx]
    except:
        break

    print('turn-%4d(%4d)' % (turn, idx), data)
    if 'call' in data:
        try:
            ret_pos = idx
            idx = proc_starts[data[1]]
        except:
            None
    elif 'ujp' in data:
        idx = label_starts[data[1]]
    elif 'proc' in data:
        idx = proc_starts[data[0]]
    elif 'nop' in data:
        idx = label_starts[data[0]]
    elif 'ret' in data:
        idx = ret_pos

    idx += 1
    turn += 1