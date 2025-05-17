#!/usr/bin/env python3

import sys, bisect

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    it = iter(data)
    n = int(next(it))
    items = []
    for _ in range(n):
        ai = int(next(it)); bi = int(next(it))
        items.append((ai, bi))
    # ordenar por posición
    items.sort()
    a = [x for x, _ in items]
    b = [y for _, y in items]
    r = [0] * (n + 1)
    max_r = 0
    for k in range(n):
        L = a[k] - b[k]
        # primera posición >= L
        pos = bisect.bisect_left(a, L)
        r[k+1] = r[pos] + 1
        if r[k+1] > max_r:
            max_r = r[k+1]
    # resultado: láseres destruidos = total - supervivientes óptimos
    print(n - max_r)


if __name__ == '__main__':
    main()
