#!/usr/bin/env python3
import sys
import math


def inp():
    return sys.stdin.readline().strip()


def get_int():
    return int(inp())


def get_ints():
    return list(map(int, inp().split()))

def solve(p, d):
    len_ = len(d)
    el = [0] * len_

    for i in range(1, len(p)):
        tot = 0
        m = i
        j = i - 1
        while j >= 0 and m >= 0:
            if p[j] >= p[m] - d[m]:
                tot += 1
                j -= 1
            else:
                tot += el[j]
                break
        el[i] = tot 
    for i in range(len_):
        el[i] = el[i]+ len_ - 1 -i

    return min(el)

def main():
    s = get_int()
    d = []
    p = []
    for i in range(s):
        ls = get_ints()
        d.append(ls[0])
        p.append(ls[1])

    print(solve(d, p))


if __name__ == '__main__':
    main()
