arr = [1,2,3,4,5,6,7,8,9,10]
result = []
file_len = 6 # header_len = 4

file_start_pos = len(arr) - file_len
result.append(arr[0:file_start_pos])
result.append(arr[file_start_pos:])

print(result)

if len(result[0]) > 0:
    None
else:
    None    

print(result)