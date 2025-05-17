#!/usr/bin/env python3
import sys
import math


def inp():
    return sys.stdin.readline().strip()


def get_int():
    return int(inp())


def get_ints():
    return list(map(int, inp().split()))

def solve(n, k, ds):
    concurrent = 0
    max_n_conc = -1
    for i in range(n):
        while ds[i] >= ds[concurrent] + 1000:
            concurrent += 1
        n_concurrent = abs(concurrent - i) + 1
        if n_concurrent > max_n_conc:
            max_n_conc = n_concurrent
    serv = int(math.ceil(max_n_conc / k))
    return serv

def main():
    t = get_ints()
    ds = []
    for i in range(t[0]):
        ds.append(get_int())
    print(solve(t[0], t[1], ds))

    
    


if __name__ == '__main__':
    main()
