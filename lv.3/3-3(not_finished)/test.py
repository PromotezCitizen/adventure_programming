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

    for line in converted_lines:
        print(line)

    return converted_lines

def getUCODESplitedByProc(ucode_data):
    function_line = []
    temp = []
    for idx, line in enumerate(ucode_data):
        if 'proc' not in line:
            temp.append(line)
            continue
        function_line.append(temp)
        temp = []
        temp.append(line)
        # print('%3d\t' % (idx+1), 'proc' in line)
        
    if len(temp) > 0:
        function_line.append(temp)

    for idx ,line in (enumerate(function_line)):
        print(line[0])
        print('%3d\t' % (idx+1), 'proc' in line[0])

    return function_line

ucode = getUCODEData()
ucode = getUCODESplitedByProc(ucode)

# for idx, line in enumerate(lines):
#     if 'proc' not in line:
#         temp.append(line)
#         continue
#     function_line.append(temp)
#     temp = []
#     temp.append(line)
#     # print('%3d\t' % (idx+1), 'proc' in line)
# function_line.append(temp)

# for idx ,line in (enumerate(function_line)):
#     print(line[0])
#     print('%3d\t' % (idx+1), 'proc' in line[0])