#!/usr/bin/env python3
import sys
import math
from collections import deque

def inp():
    return sys.stdin.readline().strip()


def get_int():
    return int(inp())


def get_ints():
    return list(map(int, inp().split()))
def reb(d1, d2, x):
    l1 = len(d1)
    l2 = len(d2)
    while l1 > x:
        d2.appendleft(d1.pop())
        l2 += 1
        l1 -= 1
    while l2 > x + 1:
        d1.append(d2.popleft())
        l2 -= 1
        l1 += 1
def main1():
    n = get_int()
    d1 = deque()
    d2 = deque()

    for i in range(n):
        op = inp()
        op = op.split(' ')
        x = int(op[1])
        l1 = len(d1)
        l2 = len(d2)
        idx_x = (l1 + l2 + 1) // 2

        if op[0][0] == 'g':
            if x < l1:
                print(d1[x])
            else:
                print(d2[x - l1])
        elif op[0][5] == 'b':
            d2.append(x)
            idx_x = (l1 + l2 + 1) // 2
            reb(d1, d2, idx_x)
        elif op[0][5] == 'f':
            d1.appendleft(x)
            idx_x = (l1 + l2 + 1) // 2
            reb(d1, d2, idx_x)
        else:
            if idx_x == l1:
                d2.appendleft(x)
            elif idx_x > l1:
                d1.append(d2.popleft())
                d2.appendleft(x)
            idx_x = (l1 + l2 + 1) // 2
            reb(d1, d2, idx_x)
        # print("----------")
        # print(d1, d2)
        # print("----------")
def main():
    n = get_int()
    animals = []
    for i in range(n):
        animals.append(inp())
    len_a = len(animals)
    res = 0

    for i in reversed(range(len_a)):
        if animals[i] == 'O':
            res += 2**(len_a - i - 1)

    print(res)
if __name__ == '__main__':
    main()

