class UCodeInterpreter():
    def __init__(self, folder, file):
        self.__folder_path = folder
        self.__file_path = file
        self.__ucode = None
        self.__proc_starts = None
        self.__label_starts = None
        self.__stack = []
        self.__mem = []

    def run(self):
        self.__ucode = self._getUCODEData()
        self.__proc_starts = self._getStartPosition(self.__ucode, 'proc')
        self.__label_starts = self._getStartPosition(self.__ucode, 'nop')
        print(self.__proc_starts, self.__label_starts)
        self._runUcode()
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

    def _runUcode(self):
        turn = 0
        idx = 0
        ret_pos = None
        while turn < 200:
            try:
                data = self.__ucode[idx]
            except:
                break

            print('turn-%4d(%4d)' % (turn, idx), data)
            if 'call' in data:
                try:
                    ret_pos = idx
                    idx = self.__proc_starts[data[1]]
                except:
                    None
            elif 'ujp' in data:
                idx = self.__label_starts[data[1]]
            elif 'proc' in data:
                idx = self.__proc_starts[data[0]]
            elif 'nop' in data:
                idx = self.__label_starts[data[0]]
            elif 'ret' in data:
                idx = ret_pos

            idx += 1
            turn += 1

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
        
        # if 'call' in data:
        #     try:
        #         ret_pos = idx
        #         idx = proc_starts[data[1]]
        #     except:
        #         None

        # elif 'proc' in data:
        #     idx = proc_starts[data[0]]

        # elif 'nop' in data:
        #     idx = label_starts[data[0]]

        # elif 'ret' in data:
        #     idx = ret_pos
        
def start():

    def funcOperation(line):
        if line[0] == 'proc':
            None
        elif line[0] == 'ret':
            None
        elif line[0] == 'ldp':
            None
        elif line[0] == 'push':
            None
        else: # call
            None 

    def ioOperation(line):
        None

    # 데이터 이동 연산
    def datmvOperation(line):
        if line[0] == 'lod':
            None
            # blck = line[1]
            # ofst = line[2]
            # stack.append(mem[blck][ofst])

        elif line[0] == 'lda':
            None
            # blck = line[1]
            # ofst = line[2]
            # stack.append([blck, ofst])
            # 나중에 mem[blck][ofst]으로 연산
        elif line[0] == 'ldc':
            None
            # stack.append(line[1])
        elif line[0] == 'str':
            None
            # blck = line[1]
            # ofst = line[2]
            # mem[blck][ofst] = stack.pop()
        elif line[0] == 'ldi':
            None
            # arr = stack.pop()
            # blck = arr[0]
            # ofst = arr[1]
            # stack.append(mem[blck][ofst])
        else: # sti
            None
            # data = stack.pop()
            # arr = stack.pop()
            # blck = arr[0]
            # ofst = arr[1]
            # mem[blck][ofst] = data


    # 단항 연산
    def unaryOperation(line): # 스택을 직접 수정한다 가정
        if line[0] == 'not':
            None
            #stack[-1] = not stack[-1]
        elif line[0] == 'neg':
            None
            #stack[-1] = -stack[-1]
        elif line[0] == 'inc':
            None
            #stack[-1] += 1
        elif line[0] == 'dec':
            None
            #stack[-1] -= 1
        else: # dup
            None
            #stack.append(stack[-1])

    # 이항 연산 - eval 사용
    # swap도 추가해야한다
    def binaryOperation(line): # 스택을 직접 수정한다 가정
        if line[0] == 'swp':
            None
            # tmp = stack[-1]
            # stack[-1] = stack[-2]
            # stack[-2] = tmp
        else:
            data = None
            try:
                if len(stack[-1] > 1):
                    None
                    # arr = stack.pop()
                    # blck = arr[0]
                    # ofst = arr[1]
                    # idx = mem[line[1]][line[2]]
                    # stack.append([blck, ofst+idx])
            except:
                None
                # data = eval('{0} {1} {2}'.format(
                #         stack[-2],
                #         binary_operators[line[0]],
                #         stack[-1]
                #     ))
            finally:
                None
                # stack.append(data)
    
    # 흐름 제어
    def jmpOperation(line, idx):
        if line[0] == 'fjp':
            None
            # flag = stack.pop()
            # if flag == False:
            #     idx = label_starts[data[1]]
        elif line[0] == 'tjp':
            None
            # flag = stack.pop()
            # if flag == True:
            #     idx = label_starts[data[1]]
        else: # ujp
            idx = label_starts[line[1]]

        return idx

    ucode = getUCODEData()
    proc_starts = getStartPosition(ucode, 'proc')
    label_starts = getStartPosition(ucode, 'nop')

    turn = 0
    idx = 0
    ret_pos = None

    global stack
    global mem

    while turn < 200: # data[0] != 'end'
        data = ucode[idx]
        # try:
        #     data = ucode[idx]
        # except:
        #     break

        print('turn-%4d(%4d)' % (turn, idx), data)
        if data[0] in program_operators:
            None

        elif data[0] in function_operators:
            None

        elif data[0] in io_operators:
            None

        elif data[0] in datmv_operators:
            datmvOperation(data)

        elif data[0] in binary_operators.keys():
            binaryOperation(data[0])

        elif data[0] in unary_operators:
            unaryOperation(data[0])

        elif data[0] in jmp_operators:
            idx = jmpOperation(data, idx)

        idx += 1
        turn += 1



stack = []
mem = []
program_operators = [
    'nop', 'bgn', 'syn', 'end'
]
function_operators = [
    'proc', 'ret', 'ldp', 'push', 'call'
]
io_operators = [
    'read', 'write', 'lf'
]
datmv_operators = [
    'lod', 'lda', 'ldc', 'str', 'ldi', 'sti'
]
unary_operators = [
    'not', 'neg', 'inc', 'dec', 'dup'
]
binary_operators = {
    'add': '+',
    'sub': '-',
    'mult': '*',
    'div': '/',
    'mod': '%',
    'gt': '<',
    'lt': '>',
    'ge': '<=',
    'le': '>=',
    'eq': '==',
    'ne': '!=',
    'and': 'and',
    'or': 'or'
}
jmp_operators = [
    'ujp', 'tjp', 'fjp'
]
start()
