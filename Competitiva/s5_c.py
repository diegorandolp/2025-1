#!/usr/bin/env python3
import sys
import math
            

def inp():
    return sys.stdin.readline().strip()


def get_int():
    return int(inp())

def get_ints():
    return list(map(int, inp().split()))

def solve(n, nums, k):
    cost = [0] * n
    last_idx = [-1] * n
    for i in range(1, n):
        min_idx = i-1
        min_cost = cost[i-1] + abs(nums[i] - nums[i-1])
        for j in range(1, k + 1):
            if i-j >= 0:
                new_cost = cost[i-j] + abs(nums[i] - nums[i-j]) 
                if new_cost < min_cost:
                    min_cost = new_cost
                    min_idx = j
        last_idx = min_idx
        cost[i] = min_cost
    return cost[n-1]


def main():
    s = get_ints()
    nums = get_ints()
    print(solve(s[0], nums, s[1]))

if __name__ == '__main__':
    main()
