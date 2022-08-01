def getUCODEData():
    folder_path = '레벨3.3 UCode테스트/'
    file_path = 'test1.uco'

    # https://wikidocs.net/26 - readlines
    with open(folder_path+file_path, 'r') as f:
        raw_lines = f.readlines()

    trimed_lines = []
    for line in raw_lines:
        # https://velog.io/@xdfc1745/Mote-python-%EC%8A%A4%ED%8A%B8%EB%A7%81-trim - str trim
        trimed_lines.append([ x for x in line.rstrip().split(' ') if x is not ''])

    converted_lines = []
    for line in trimed_lines:
        temp = []
        for data in line:
            try: data = int(data)
            except: None
            finally: temp.append(data)
        converted_lines.append(temp)

    return converted_lines

def getUCODESplitedByName(ucode_data, name):
    function_block = []
    temp = []
    for line in ucode_data:
        
        if name not in line:
            temp.append(line)
            continue
        function_block.append(temp)
        temp = []
        temp.append(line)

    if len(temp) > 0:
        function_block.append(temp)

    return function_block

ucode = getUCODEData()
ucode = getUCODESplitedByName(ucode, 'proc')

program = []
for line in ucode:
    program.append(getUCODESplitedByName(ucode, 'nop'))


print(len(program))

for blocks in program:
    for block in blocks:
        for lines in block:
            for line in lines:
                printer = '\t\t'
                if 'proc' in line:
                    printer = ''
                elif 'nop' in line:
                    printer = '\t'
                print(printer, line)