#!/usr/bin/env python3
import sys
import math


def inp():
    return sys.stdin.readline().strip()
def pot(x,n):
    if n == 0 :
        return 1
    y = pot(x, n//2)
    y = (y ** 2) % 10000007
    if n % 2:
        y = (y% 10000007)*(x% 10000007 )
    return y % 10000007


def get_int():
    return int(inp())


def get_ints():
    return list(map(int, inp().split()))

def bs(nums, start, end, key):
    if start > end: 
        return -1
    m_idx = (start + end) // 2
    if key == nums[m_idx]:
        return m_idx
    elif key < nums[m_idx]:
        return bs(nums, start, m_idx-1, key)
    else:
        return bs(nums, m_idx+1, end, key)
#10 = 3 * a+ca
#4 = 0 * b+c*b
#4 = (-1)*m +c*m
#5 = a+b+m
def solve(n, k):
    m = 10000007

    a_1 = pow(n-1, n-1, m)
    a_2 = pow(n-1, k, m)

    b_1 = pow(n, n, m) 

    b_2 = pow(n, k, m)


    c_1 = ((a_1+a_2) + b_1+b_2)% m


    c_2 = (a_1+a_2) % m


    return (c_1 + c_2) % m

   
def main():
    #s = get_int()
    #for i in range(s):
    #    n = get_ints()
    #    print(pot(n[0] , n[1] ))
    s = get_ints()
    while s[0] != 0 or s[1] != 0:
        print(solve(s[0], s[1]))
        s = get_ints()


if __name__ == '__main__':
    main()
