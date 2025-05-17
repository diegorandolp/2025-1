#!/usr/bin/env python3
import sys
import math


def inp():
    return sys.stdin.readline().strip()


def get_int():
    return int(inp())


def get_ints():
    return list(map(int, inp().split()))

def main():
    nums = []
    s = get_ints()

    while(s != ""){
        nums.append(s)
        s = get_ints()
    }


if __name__ == '__main__':
    main()
