class Operators():
    def __init__(self):
        self.__program_operators = [
            'nop', 'bgn', 'sym', 'end'
        ]
        self.__function_operators = [
            'proc', 'ret', 'ldp', 'push', 'call'
        ]
        self.__io_operators = [
            'read', 'write', 'lf'
        ]
        self.__datmv_operators = [
            'lod', 'lda', 'ldc', 'str', 'ldi', 'sti'
        ]
        self.__unary_operators = [
            'not', 'neg', 'inc', 'dec', 'dup'
        ]
        self.__binary_operators = {
            'add': '+',
            'sub': '-',
            'mult': '*',
            'div': '/',
            'mod': '%',
            'gt': '>',
            'lt': '<',
            'ge': '>=',
            'le': '<=',
            'eq': '==',
            'ne': '!=',
            'and': 'and',
            'or': 'or'
        }
        self.__jmp_operators = [
            'ujp', 'tjp', 'fjp'
        ]

    def isProgramOp(self, op):
        return op in self.__program_operators
    
    def getProgramOp(self):
        return self.__program_operators

    def isFuncOp(self, op):
        return op in self.__function_operators

    def getFuncOp(self):
        return self.__program_operators
    
    def isIoOp(self, op):
        return op in self.__io_operators

    def getIoOp(self):
        return self.__io_operators
    
    def isDataOp(self, op):
        return op in self.__datmv_operators

    def getDataOp(self):
        return self.__datmv_operators
    
    def isUnaryOp(self, op):
        return op in self.__unary_operators

    def getUnaryOp(self):
        return self.__unary_operators
    
    def isBinaryOp(self, op):
        return op in self.__binary_operators

    def getBinaryOp(self):
        return self.__binary_operators
    
    def isJmpOp(self, op):
        return op in self.__jmp_operators
    
    def getJmpOp(self):
        return self.__jmp_operators

class UCodeCommand(Operators):
    def __init__(self, ucode, proc_starts, label_starts, stack, mem, params):
        super().__init__()
        self._ucode = ucode
        self._proc_starts = proc_starts
        self._label_starts = label_starts
        self._stack = stack
        self._mem = mem
        self._idx = 0
        self.__call_proc_mem = []
        self._params = params

    def _programOperation(self, line):
        if line[1] == 'nop':
            None
        elif line[0] == 'bgn':
            None
        elif line[0] == 'sym':
            if len(self._params) > 1:
                try:
                    self._mem[2].append(self._params[line[2]])
                except:
                    for idx in range(line[3]):
                        # self._mem[line[1]][line[2]+idx] = 0
                        self._mem[line[1]].append(0)     
            else:
                for idx in range(line[3]):
                    # self._mem[line[1]][line[2]+idx] = 0
                    self._mem[line[1]].append(0)
        else: # end
            None

    def _funcOperation(self, line, idx, ret_pos):
        command = line[0]
        idx = idx
        if command == 'proc':
            None

        elif command == 'ret':
            idx = ret_pos+1

        elif command == 'ldp':
            self.__call_proc_mem = []

        elif command == 'push':
            self.__call_proc_mem.append(self._stack.pop())

        else: # call
            procedure = line[1]
            ret_pos = idx
            
            if self.isIoOp(procedure):
                self._ioOperation(procedure)
            else:
                # ucode, proc_starts, label_starts, stack, mem, idx
                UCodeProc(self._ucode,
                    self._proc_starts, self._label_starts,
                    self._stack, self._mem, # self.__call_proc_mem
                    self._proc_starts[procedure],
                    self.__call_proc_mem).run()
                # idx = self._proc_starts[procedure]
        return idx, ret_pos

    def _ioOperation(self, procedure):
        if procedure == 'read':
            data = int(input("input data >> "))
            self._stack.append(data)
        elif procedure == 'write':
            print(self._stack[-1])
        elif procedure == 'lf':
            print('')

    # 데이터 이동 연산
    def _datmvOperation(self, line):
        if line[0] == 'lod':
            blck = line[1]
            ofst = line[2]
            self._stack.append(self._mem[blck][ofst])

        elif line[0] == 'lda':
            blck = line[1]
            ofst = line[2]
            self._stack.append([blck, ofst])
            # 나중에 mem[blck][ofst]으로 연산. 실제로는 mem[0][1]

        elif line[0] == 'ldc':
            self._stack.append(line[1])

        elif line[0] == 'str':
            blck = line[1]
            ofst = line[2]
            data = self._stack[-1]
            self._mem[blck][ofst] = data

        elif line[0] == 'ldi':
            arr = self._stack.pop()
            print(arr, self._mem)
            blck = arr[0]
            ofst = arr[1]
            self._stack.append(self._mem[blck][ofst])

        else: # sti
            data = self._stack.pop()
            arr = self._stack.pop()
            blck = arr[0]
            ofst = arr[1]
            self._mem[blck][ofst] = data
        #print('stack:', self._stack) 

    # 단항 연산
    def _unaryOperation(self, line): # 스택을 직접 수정한다 가정
        if line[0] == 'not':
            self._stack[-1] = not self._stack[-1]
        elif line[0] == 'neg':
            self._stack[-1] = -self._stack[-1]
        elif line[0] == 'inc':
            self._stack[-1] += 1
        elif line[0] == 'dec':
            self._stack[-1] -= 1
        else: # dup
            self._stack.append(self._stack[-1])

    # 이항 연산 - eval 사용
    # swap도 추가해야한다
    def _binaryOperation(self, line): # 스택을 직접 수정한다 가정
        if line[0] == 'swp':
            tmp = self._stack[-1]
            self._stack[-1] = self._stack[-2]
            self._stack[-2] = tmp
        else:
            data = None
            try:
                if len(self._stack[-1]) > 1: # lod lda add인 경우
                    arr = self._stack.pop()
                    idx = self._stack.pop()

                    blck = arr[0]
                    ofst = arr[1]

                    # idx = self._mem[line[1]][line[2]] # line을 다른걸로 처리 가능해야함
                    # 2개 pop 해서 인덱스 연산
                    print(arr, idx)
                    data = [blck, ofst+idx]
            except:
                right_data = self._stack.pop()
                left_data = self._stack.pop()
                # print('%3d %s %3d' % (left_data, self.getBinaryOp()[line[0]], right_data))
                data = eval('{0} {1} {2}'.format(
                        left_data,
                        self.getBinaryOp()[line[0]],
                        right_data
                    ))
            finally:
                self._stack.append(data)
    
    # 흐름 제어
    def _jmpOperation(self, line, idx):
        if line[0] == 'fjp':
            flag = self._stack.pop()
            if flag == False:
                idx = self._label_starts[line[1]]
        elif line[0] == 'tjp':
            flag = self._stack.pop()
            if flag == True:
                idx = self._label_starts[line[1]]
        else: # ujp
            idx = self._label_starts[line[1]]

        return idx

class UCodeProc(UCodeCommand):
    def __init__(self, ucode, proc_starts, label_starts, stack, mem, idx, params):
        super().__init__(ucode,
            proc_starts, label_starts,
            stack, mem,
            params) # [ [ -1 for _ in range(30) ] for _ in range(3) ], [ [] for _ in range(3)]
        mem[-1] = []
        self.__params = params
        self._idx = idx
        # ucode, proc_starts, label_starts, stack, mem

    def run(self):
        turn = 0
        ret_pos = 0

        print(self._proc_starts)
        print(self._label_starts)

        while True: # data[0] != 'end'
            data = self._ucode[self._idx]
            if data[0] == 'ret':
                break
            print('turn-%4d(%4d)' % (turn, self._idx), data)

            op = data[0]
            if self.isProgramOp(op):
                self._programOperation(data)

            elif self.isFuncOp(op):
                self._idx, ret_pos = self._funcOperation(data, self._idx, ret_pos)

            elif self.isDataOp(op):
                self._datmvOperation(data)

            elif self.isUnaryOp(op):
                self._unaryOperation(data)

            elif self.isBinaryOp(op):
                self._binaryOperation(data)

            elif self.isJmpOp(op):
                self._idx = self._jmpOperation(data, self._idx)

            self._idx += 1
            turn += 1
    
            print('\t%5s:' % 'stack ', self._stack)
            print('\t%5s:' % 'mem')
            for dat in self._mem:
                print('\t\t', dat)      



class UCodeInterpreter(UCodeCommand):
    def __init__(self, folder, file):
        mem = [ [] for _ in range(3)]
        super().__init__(None, None, None, [], mem, [])
        self.__folder_path = folder
        self.__file_path = file

    def run(self):
        self._ucode = self._getUCODEData()
        self._proc_starts = self._getStartPosition(self._ucode, 'proc')
        self._label_starts = self._getStartPosition(self._ucode, 'nop')
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
        ret_pos = 0

        print(self._proc_starts)
        print(self._label_starts)

        while True: # data[0] != 'end'
            data = self._ucode[idx]
            if data[0] == 'end':
                break
            print('turn-%4d(%4d)' % (turn, idx), data)

            op = data[0]
            if self.isProgramOp(op):
                self._programOperation(data)

            elif self.isFuncOp(op):
                idx, ret_pos = self._funcOperation(data, idx, ret_pos)

            elif self.isDataOp(op):
                self._datmvOperation(data)

            elif self.isUnaryOp(op):
                self._unaryOperation(data)

            elif self.isBinaryOp(op):
                self._binaryOperation(data)

            elif self.isJmpOp(op):
                idx = self._jmpOperation(data, idx)

            idx += 1
            turn += 1
'''
    # def _programOperation(self, line):
    #     if line[1] == 'nop':
    #         None
    #     elif line[0] == 'bgn':
    #         None
    #     elif line[0] == 'sym':
    #         for _ in range(line[3]):
    #             self.__mem[line[1]].append(-1)
    #     else: # end
    #         None

    # def _funcOperation(self, line, idx, ret_pos):
    #     command = line[0]
    #     idx = idx
    #     if command == 'proc':
    #         None

    #     elif command == 'ret':
    #         idx = ret_pos+1

    #     elif command == 'ldp':
    #         None

    #     elif command == 'push':
    #         None

    #     else: # call
    #         procedure = line[1]
    #         ret_pos = idx
    #         if procedure in io_operators:
    #             self._ioOperation(procedure)
    #         else:
    #             idx = self.__proc_starts[procedure]
    #     return idx, ret_pos

    # def _ioOperation(self, procedure):
    #     if procedure == 'read':
    #         data = int(input("input data >> "))
    #         self.__stack.append(data)
    #     elif procedure == 'write':
    #         print(self.__stack[-1])
    #     elif procedure == 'lf':
    #         print('')

    # # 데이터 이동 연산
    # def _datmvOperation(self, line):
    #     submem = []
    #     if line[0] == 'lod':
    #         blck = line[1]
    #         ofst = line[2]
    #         self.__stack.append(self.__mem[blck][ofst])

    #     elif line[0] == 'lda':
    #         blck = line[1]
    #         ofst = line[2]
    #         self.__stack.append([blck, ofst])
    #         # 나중에 mem[blck][ofst]으로 연산

    #     elif line[0] == 'ldc':
    #         self.__stack.append(line[1])

    #     elif line[0] == 'str':
    #         blck = line[1]
    #         ofst = line[2]
    #         data = stack[-1]
    #         self.__mem[blck][ofst] = data

    #     elif line[0] == 'ldi':
    #         arr = stack.pop()
    #         print('\t\t', arr, stack)
    #         blck = arr[0]
    #         ofst = arr[1]
    #         self.__stack.append(mem[blck][ofst])

    #     else: # sti
    #         data = stack.pop()
    #         arr = stack.pop()
    #         blck = arr[0]
    #         ofst = arr[1]
    #         self.__mem[blck][ofst] = data
        
    #     print('stack:', self.__stack)


    # # 단항 연산
    # def _unaryOperation(self, line): # 스택을 직접 수정한다 가정
    #     if line[0] == 'not':
    #         self.__stack[-1] = not self.__stack[-1]
    #     elif line[0] == 'neg':
    #         self.__stack[-1] = -self.__stack[-1]
    #     elif line[0] == 'inc':
    #         self.__stack[-1] += 1
    #     elif line[0] == 'dec':
    #         self.__stack[-1] -= 1
    #     else: # dup
    #         self.__stack.append(self.__stack[-1])

    # # 이항 연산 - eval 사용
    # # swap도 추가해야한다
    # def _binaryOperation(self, line): # 스택을 직접 수정한다 가정
    #     if line[0] == 'swp':
    #         tmp = self.__stack[-1]
    #         self.__stack[-1] = self.__stack[-2]
    #         self.__stack[-2] = tmp
    #     else:
    #         data = None
    #         try:
    #             if len(self.__stack[-1] > 1):
    #                 arr = self.__stack.pop()
    #                 blck = arr[0]
    #                 ofst = arr[1]
    #                 idx = self.__mem[line[1]][line[2]]
    #                 self.__stack.append([blck, ofst+idx])
    #         except:
    #             right_data = self.__stack.pop()
    #             left_data = self.__stack.pop()
    #             data = eval('{0} {1} {2}'.format(
    #                     left_data,
    #                     self.__op.getBinaryOp(line[0]),
    #                     right_data
    #                 ))
    #         finally:
    #             None
    #             self.__stack.append(data)
    
    # # 흐름 제어
    # def _jmpOperation(self, line, idx):
    #     if line[0] == 'fjp':
    #         flag = self.__stack.pop()
    #         if flag == False:
    #             idx = self.__label_starts[line[1]]
    #     elif line[0] == 'tjp':
    #         flag = self.__stack.pop()
    #         if flag == True:
    #             idx = self.__label_starts[line[1]]
    #     else: # ujp
    #         idx = self.__label_starts[line[1]]

    #     return idx
'''
interpreter = UCodeInterpreter('레벨3.3 UCode테스트/', 'test1.uco')
interpreter.run()




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


def subroutine():
    None

def start():
    def programOperation(line):
        if line[1] == 'nop':
            None
        elif line[0] == 'bgn':
            None
        elif line[0] == 'sym':
            for _ in range(line[3]):
                mem[line[1]].append(-1)
        else: # end
            None

    def funcOperation(line, idx, ret_pos):
        command = line[0]
        idx = idx
        if command == 'proc':
            None

        elif command == 'ret':
            idx = ret_pos+1

        elif command == 'ldp':
            None

        elif command == 'push':
            None

        else: # call
            procedure = line[1]
            ret_pos = idx
            if procedure in io_operators:
                ioOperation(procedure)
            else:
                idx = proc_starts[procedure]
        return idx, ret_pos

    def ioOperation(procedure):
        if procedure == 'read':
            data = int(input("input data >> "))
            stack.append(data)
        elif procedure == 'write':
            print(stack[-1])
        elif procedure == 'lf':
            print('')

    # 데이터 이동 연산
    def datmvOperation(line):
        submem = []
        if line[0] == 'lod':
            blck = line[1]
            ofst = line[2]
            stack.append(mem[blck][ofst])

        elif line[0] == 'lda':
            blck = line[1]
            ofst = line[2]
            stack.append([blck, ofst])
            # 나중에 mem[blck][ofst]으로 연산

        elif line[0] == 'ldc':
            stack.append(line[1])

        elif line[0] == 'str':
            blck = line[1]
            ofst = line[2]
            data = stack[-1]
            mem[blck][ofst] = data

        elif line[0] == 'ldi':
            arr = stack.pop()
            print('\t\t', arr, stack)
            blck = arr[0]
            ofst = arr[1]
            stack.append(mem[blck][ofst])

        else: # sti
            data = stack.pop()
            arr = stack.pop()
            blck = arr[0]
            ofst = arr[1]
            mem[blck][ofst] = data
        
        print('stack:', stack)


    # 단항 연산
    def unaryOperation(line): # 스택을 직접 수정한다 가정
        if line[0] == 'not':
            stack[-1] = not stack[-1]
        elif line[0] == 'neg':
            stack[-1] = -stack[-1]
        elif line[0] == 'inc':
            stack[-1] += 1
        elif line[0] == 'dec':
            stack[-1] -= 1
        else: # dup
            stack.append(stack[-1])

    # 이항 연산 - eval 사용
    # swap도 추가해야한다
    def binaryOperation(line): # 스택을 직접 수정한다 가정
        if line[0] == 'swp':
            tmp = stack[-1]
            stack[-1] = stack[-2]
            stack[-2] = tmp
        else:
            data = None
            try:
                if len(stack[-1] > 1):
                    arr = stack.pop()
                    blck = arr[0]
                    ofst = arr[1]
                    idx = mem[line[1]][line[2]]
                    stack.append([blck, ofst+idx])
            except:
                right_data = stack.pop()
                left_data = stack.pop()
                data = eval('{0} {1} {2}'.format(
                        left_data,
                        binary_operators[line[0]],
                        right_data
                    ))
            finally:
                None
                stack.append(data)
    
    # 흐름 제어
    def jmpOperation(line, idx):
        if line[0] == 'fjp':
            flag = stack.pop()
            if flag == False:
                idx = label_starts[line[1]]
        elif line[0] == 'tjp':
            flag = stack.pop()
            if flag == True:
                idx = label_starts[line[1]]
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

    print(proc_starts)
    print(label_starts)

    while turn < 200: # data[0] != 'end'
        data = ucode[idx]

        print('turn-%4d(%4d)' % (turn, idx), data)

        if data[0] in program_operators:
            programOperation(data)

        elif data[0] in function_operators:
            idx, ret_pos = funcOperation(data, idx, ret_pos)

        elif data[0] in datmv_operators:
            datmvOperation(data)

        elif data[0] in unary_operators:
            unaryOperation(data)

        elif data[0] in binary_operators.keys():
            binaryOperation(data)

        elif data[0] in jmp_operators:
            idx = jmpOperation(data, idx)

        idx += 1
        turn += 1
        
        # print('\tturn-%4d(%4d)' % (turn, idx), data)

stack = []
mem = [[] for _ in range(3)]



program_operators = [
    'nop', 'bgn', 'sym', 'end'
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
# start()
