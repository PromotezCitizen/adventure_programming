



size = 4

chess_map = [
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 0, 1]
]
# 2,2 start => (0,0), (1,1), (2,2), (3,3)
# 2,1 start => (0,-1), (1,0), (2,1), (3,2) => col start = col-row

size = 5

chess_map = [
    [1, 0, 0, 0, 0],
    [0, 1, 0, 0, 0],
    [0, 1, 0, 0, 0],
    [0, 0, 0, 1, 0],
    [0, 0, 1, 0, 0]
]

pos_row = 4
pos_col = 2
# 4,3
# 

# 정의
#   위쪽 : 수직방향에서 인덱스의 크기가 작아지는 방향
#   아래쪽 : 수직방향에서 인덱스의 크기가 커지는 방향
#   pos : 양의 기울기
#   neg : 음의 기울기
print('current pos - row: %d, col: %d' % (pos_row, pos_col))
vertical_map = [
    x[pos_col]
    for idx, x in enumerate(chess_map)
        if (idx < pos_row)
] # 현재 위치의 위쪽에 있는 체스판만 생각
print('virtical', sum(vertical_map), vertical_map)

check_neg = pos_col - pos_row
cross_map_11_to_5 = [
    x[check_neg + idx]
    for idx, x in enumerate(chess_map)
        if (check_neg + idx > -1) and (idx < pos_row)
]
print('cross-11 to 5', sum(cross_map_11_to_5), cross_map_11_to_5)

check_pos = pos_row + pos_col
cross_map_1_to_7 = [
    x[check_pos - idx] 
    for idx, x in enumerate(chess_map)
        if (check_pos - idx < size) and (idx < pos_row)
]
print('cross-1 to 7', sum(cross_map_1_to_7), cross_map_1_to_7)

# row = 2, col = 1
# calc 11 to 5
#       row = 1, col = 0
#       row = 3, col = 2
#       
# calc 1 to 7 => sum = 3 => row+col
#       row = 0, col = 3
#       row = 1, col = 2
#       row = 3, col = 0


# row = 1, col = 1
# calc 11 to 5
#       row = 0, col = 0
#       row = 2, col = 2
#       row = 3, col = 3
#       
# calc 1 to 7 => sum = 2 => row+col
#       row = 0, col = 2
#       row = 2, col = 0


# if map == [5][5]


# row = 2, col = 1
# calc 11 to 5
#       row = 0, col = -1 <= invalid.
#       row = 1, col = 0
#       row = 3, col = 2
#       row = 4, col = 3
#       
# calc 1 to 7 => sum = 3 => row+col
#       row = 0, col = 3
#       row = 1, col = 2
#       row = 3, col = 0


# row = 1, col = 1
# calc 11 to 5
#       row = 0, col = 0 => col_start = col-row
#       row = 2, col = 2
#       row = 3, col = 3
#       row = 4, col = 4
#       
# calc 1 to 7 => sum = 2 => row+col
#       row = 0, col = 2
#       row = 2, col = 0

# row = 2, col = 3
# calc 11 to 5
#       row = 0, col = 1
#       row = 2, col = 2
#       row = 3, col = 3
#       row = 4, col = 4
#       
# calc 1 to 7 => sum = 5 => row+col
#       row = 1, col = 4
#       row = 3, col = 2
#       row = 4, col = 1