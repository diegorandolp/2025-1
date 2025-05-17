#!/usr/bin/env python3
import sys
import math
import heapq

def inp():
    return sys.stdin.readline().strip()


def get_int():
    return int(inp())


def get_ints():
    return list(map(int, inp().split()))
def solve(n, t, vpt):
    tot = 0
    cands = []
    for i in range(t-1, -1, -1):
        if len(vpt[i]) != 0:
            for m in vpt[i]:
                heapq.heappush(cands, -m)
            if len(cands) != 0:
                tot += -heapq.heappop(cands)
    return tot
def main():
    s = get_ints()
    ins = [[] for i in range(s[1])]
    for i in range(s[0]):
        val = get_ints()
        ins[val[1]].append(val[0])
    print(solve(s[0], s[1], ins))


if __name__ == '__main__':
    main()
