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
    s = inp()
    length = len(s)

    letters = {}
    for ch in s:
        letters[ch] = letters.get(ch, 0) + 1
    new_s = ['-1'] * length
    impares = []
    start = 0

    for i in range(length):
        new_s[i] = letters.get(s[i], 0)

    for key in letters:
        if letters[key] % 2 == 0:
            for i in range(letters[key] // 2):
                new_s[start + i] = key
                new_s[-1 - (start + i)] = key
            start += letters[key] // 2
        else:
            impares.append(key)

    if len(impares) > 1:
        print('NO SOLUTION')
    else:
        for i in range(letters[impares[0]]):
            new_s[start + i] = impares[0]
        print("".join(new_s))






if __name__ == '__main__':
    main()
