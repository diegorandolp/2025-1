#!/usr/bin/env python3
import sys

def inp():
    return sys.stdin.readline().strip()

def get_int():
    return int(inp())

def get_ints():
    return list(map(int, inp().split()))
possible_nums = []
def get_num(board, i_l, j_l, num):
    if len(num) == 3:
        possible_nums.append(int(num))
    else:
        if len(num) > 0:
            possible_nums.append(int(num))
        for i in range(i_l, 4):
            for j in range(j_l, 3):
                if board[i][j] == -1:
                    continue
                get_num(board, i, j, num + str(board[i][j]))


def main():
    n = get_int()

    board = [
                [1, 2, 3],
                [4, 5, 6],
                [7, 8, 9],
                [-1, 0, -1]
            ]
    get_num(board, 0, 0, '')

    for i in range(n):
        num = get_int()
        near = 999
        for m in possible_nums:
            if abs(m-num) < abs(near-num):
                near = m
        print(near)



if __name__ == '__main__':
    main()

