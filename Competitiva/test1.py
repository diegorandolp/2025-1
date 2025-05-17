#!/usr/bin/env python3
import sys
import math


def inp():
    return sys.stdin.readline().strip()


def get_int():
    return int(inp())


def get_ints():
    return list(map(int, inp().split()))

def solve(a, b):
    if a == b:
        return 0
    tes = -1
    if a.count('1') == 0 :
        return -1
    if b.count('1') == 0:
        return -1
    n = len(a)

    res_ = 0
    temp = 0
    sw = 0
    same = 0
    a1b0 = 0
    a1b1 = 0


    for i in range(n):
        if a[i] != b[i]:
            sw += 1
            if a[i] == '1':
                a1b0 += 1
        else:
            same += 1
            if a[i] == '1':
                a1b1 += 1
    ans = 10**18
    ans2 = False
    if sw % 2 == 0 and a1b0 > 0:
        ans2 = True
        ans = sw 
    if same % 2 == 1 and a1b1 > 0:
    
        ans = min(ans, same)
    return ans if ans < 10**18 else -1
def main():
    t = get_int()
    for i in range(t):
        n = get_int()
        a = inp()
        b = inp()
        print(solve(a, b))

if __name__ == '__main__':
    main()
