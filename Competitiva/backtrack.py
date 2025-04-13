#!/usr/bin/env python3
'''
Example backtracking para Queens problem, based con permutations code
'''
import sys
import math


def inp():
    return sys.stdin.readline().strip()


def get_int():
    return int(inp())


def get_ints():
    return list(map(int, inp().split()))

def solve(board, i, count, diag1, diag2, cols, queens):
    if queens[0] == 8:
        count[0] = count[0] + 1
    else:
        for j in range(8):
            # Condition
            if board[i[0]][j] == '*' or diag1.get(i[0]+j, -1) != -1 or  diag2.get(i[0]+8-j, -1) != -1 or cols[j] == True:
                continue
            # Filling
            diag1[i[0]+j] = 1
            diag2[i[0]+8-j] = 1
            cols[j] = True
            queens[0] = queens[0] + 1
            i[0] = i[0] + 1
            # Deep search
            solve(board, i, count, diag1, diag2, cols, queens)
            # Restore
            i[0] = i[0] - 1
            diag1[i[0]+j] = -1
            diag2[i[0]+8-j] = -1
            cols[j] = False
            queens[0] = queens[0] - 1


def main():
    board = []
    for i in range(8):
        board.append(inp())
    
    count_ways = [0]
    queens = [0]
    i = [0]

    diag1 = {}
    diag2 = {}
    cols = [False for i in range(8)]

    solve(board, i, count_ways, diag1, diag2, cols, queens)

    print(count_ways[0])

if __name__ == '__main__':
    main()
