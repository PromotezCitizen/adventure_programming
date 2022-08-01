def getUCODEData():
    # folder_path = '레벨3.3 UCode테스트/'
    # file_path = 'test1.uco'
    folder_path = ''
    file_path = 'test.uco'

    # https://wikidocs.net/26 - readlines
    with open(folder_path+file_path, 'r') as f:
        raw_lines = f.readlines()

    trimed_lines = []
    for line in raw_lines:
        # https://velog.io/@xdfc1745/Mote-python-%EC%8A%A4%ED%8A%B8%EB%A7%81-trim - str trim
        trimed_lines.append([ x for x in line.rstrip().split(' ') if x is not ''])

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

def getFuncStartPosition(ucode, name):
    func_start = {}
    for idx, line in enumerate(ucode):
        if name in line:
            func_start[line[0]] = idx
    return func_start

ucode = getUCODEData()
proc_starts = getFuncStartPosition(ucode, 'proc')
label_starts = getFuncStartPosition(ucode, 'nop')


for data in ucode:
    print(data)