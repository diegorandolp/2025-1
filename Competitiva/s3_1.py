#!/usr/bin/env python3
import sys
import math


def inp():
    return sys.stdin.readline().strip()


def get_int():
    return int(inp())


def get_ints():
    return list(map(int, inp().split()))
def solve(let):
    up_lim = 100
    dw_lim = -100
    for j in range(dw_lim, up_lim + 1):
        for k in range(j+1, up_lim + 1):
            x = j
            y = k
            z = let[0] - (x + y)
            if x * y * z == let[1] and x ** 2 + y ** 2 + z ** 2 == let[2]:
                print(x, y, z, sep=' ')
                return
    print('No solution.')


def main():
    n = get_int()
    for i in range(n):
        let = get_ints()
        solve(let)




if __name__ == '__main__':
    main()
