#!/usr/bin/env python3
import sys
from itertools import combinations

def inp():
    return sys.stdin.readline().strip()

def get_int():
    return int(inp())

def get_ints():
    return list(map(int, inp().split()))


def main():
#    let = []
 #   for i in range(3):
#        let.append(inp())
    

#    ranges = []
#    for i in range(3):
#        ranges.append(int('9' * let[i]))
#    for i in range(ranges[0]):
#        for j in range(ranges[1]):
#            k = i + j
    n = get_int()
    points = []
    sums = {}
    for i in range(n):
        points.append(get_ints())
    for i in range(n - 1):
        for j in range(i+1, n):
            x = points[i][0] + points[j][0]
            y = points[i][1] + points[j][0]

            x = x/2
            y = y/2
            new_key = str(x) + '_' + str(y)
            sums[new_key] = sums.get(new_key, 0) + 1
    res = 0
    for key in sums:
        res += sums[key] * (sums[key] - 1) / 2
    print(int(res))



if __name__ == '__main__':
    main()

