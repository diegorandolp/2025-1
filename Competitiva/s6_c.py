#!/usr/bin/env python3
import sys
import math

MOD = 1000000007

def inp():
    return sys.stdin.readline().strip()

def get_int():
    return int(inp())


def get_ints():
    return list(map(int, inp().split()))


def summ(k, st, en):
    num = en - st + 1
    return num * (k + st - 1) + num * (num - 1) // 2


def solve(n, k):
    tot = n * k + n * (n - 1) // 2

    ma = 2 * k - 1
    disc = ma * ma + 4 * tot 
    sq = int(math.sqrt(disc))
    mi = (-ma + sq) // 2


    mi = max(1, min(n, mi))
    ans = tot 

    for i in range(mi, mi + 1):
        if 1 <= i <= n:
            pp = i * k + i * (i - 1) // 2
            diff = abs(2 * pp - tot)
            if diff < ans:
                ans = diff
    return ans


def main():
    t = get_int()
    for _ in range(t):
        n, k = get_ints()
        print("x", solve(n, k))

if __name__ == '__main__':
    main()

