#!/usr/bin/env python3
import sys
import math


def inp():
    return sys.stdin.readline().strip()


def get_int():
    return int(inp())


def get_ints():
    return list(map(int, inp().split()))

w = []
v = []
mem = [[-1] * 2001 for i in range(2001)]
choosen = []

def opt(idx, jdx):
    if idx < 0:
        return 0
    if jdx == 0:
        return 0

    if mem[idx][jdx] != -1:
        return mem[idx][jdx]
    res = 0
    if jdx < w[idx]:
        res = opt(idx-1, jdx)
    else:
        res = max(opt(idx-1,jdx), opt(idx-1,jdx-w[idx]) + v[idx])
    mem[idx][jdx] = res
    return res

def main():
    s = get_ints()
    j_init = s[0]

    for i in range(s[1]):
        item = get_ints()
        w.append(item[0])
        v.append(item[1])
    print(opt(s[1] - 1, j_init))

if __name__ == '__main__':
    main()

