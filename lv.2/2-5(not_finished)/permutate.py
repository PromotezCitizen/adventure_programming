def swap(arr, num1, num2):
    temp = arr[num1]
    arr[num1] = arr[num2]
    arr[num2] = temp

def permute(arr, start, end):
    if (start == end):
        print(arr)
        return
    else:
        for i in range(start, end+1):
            swap(arr, start, i)
            permute(arr, start+1, end)
            swap(arr, start, i)

arr_max = 3
arr = [ x for x in range(arr_max) ]
permute(arr, 0, arr_max-1)