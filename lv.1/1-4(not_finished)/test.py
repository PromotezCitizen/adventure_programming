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

result = []
for idx in range(5):
    a = len(arr)//5
    result.append(arr[idx*a:(idx+1)*a])

col_cnt = len(arr) // 5
row_cnt = len(arr) // col_cnt

arr = [ [ 0 for _ in range(row_cnt) ] for _ in range(col_cnt) ]

for row_idx, row in enumerate(result): # => row_cnt -> col_cnt, col_cnt -> row_cnt
    for col_idx, data in enumerate(row):
        print(row_idx, col_idx)
        arr[col_idx][row_cnt-row_idx-1] = data

temp = []
for data in range(len(arr)):
    temp += arr[data]

print(temp)    
for data in arr:
    print(data)
print(arr, row_cnt, col_cnt)

