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
    # Count mismatches and equal positions
    # p: a[i]=1, b[i]=0; q: a[i]=0, b[i]=1
    # eq1: a[i]=b[i]=1; eq0: a[i]=b[i]=0
    n = len(a)
    p = q = eq1 = eq0 = 0
    for ai, bi in zip(a, b):
        if ai == '1' and bi == '0':
            p += 1
        elif ai == '0' and bi == '1':
            q += 1
        elif ai == '1' and bi == '1':
            eq1 += 1
        else:  # ai == '0' and bi == '0'
            eq0 += 1
    # If already equal
    if p == 0 and q == 0:
        return 0
    # If no lit candles, cannot perform any operation
    if eq1 + p == 0:
        return -1
    ans = None
    # Direct method: use mismatches, need equal count of 1->0 and 0->1
    if p == q:
        # must have at least one 1->0 mismatch to start (ensured by eq1+p>0 and p>0)
        if p > 0:
            ans = p + q
    # Alternate method: pick equal positions (odd count), need eq1 = eq0 + 1
    # total equal positions = eq1 + eq0 must be odd
    if (eq1 + eq0) % 2 == 1 and eq1 == eq0 + 1:
        # total ops = number of equal positions
        alt = eq1 + eq0
        if ans is None or alt < ans:
            ans = alt
    return ans if ans is not None else -1
def main():
    t = get_int()
    for i in range(t):
        n = get_int()
        a = inp()
        b = inp()
        print("xx:", solve(a, b))

if __name__ == '__main__':
    main()
