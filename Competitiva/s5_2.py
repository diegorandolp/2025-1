#!/usr/bin/env python3
import sys
import math


def inp():
    return sys.stdin.readline().strip()


def get_int():
    return int(inp())


def get_ints():
    return list(map(int, inp().split()))

def opt(idx, jdx, w, v):
    mem = [[0] * (jdx+1) for i in range(idx+1)]
    # 0,j = 0; no hay items
    # i,0 = 0; no hay capacidad
    for i in range(1, idx+1):
        for j in range(jdx+1):
            if j < w[i-1]:
                mem[i][j] = mem[i-1][j]
            else:
                mem[i][j] = max(mem[i-1][j], mem[i-1][j-w[i-1]] + v[i-1])


    # back
    choosen = []
    for i in range(i_init)
    return mem[idx][jdx] 

#def get_it(i_init, j_init):
    #j = j_init
    #choosen = []
     
    #for i in range(i_init-1, -1, -1):
    #    if i == 0 and mem[0][j] > 0:
    #        choosen.append(0)
    #    elif mem[i][j] != mem[i-1][j]:
    #        choosen.append(i)
    #        j = j - w[i]
    #return choosen


def main():
    s = get_ints()
    while s:
        j_init = s[0]
        w = []
        v = []
        for i in range(s[1]):
            item = get_ints()
            w.append(item[1])
            v.append(item[0])
        print("#", opt(s[1], j_init, w, v), "#")
        s = get_ints()
if __name__ == '__main__':
    main()
