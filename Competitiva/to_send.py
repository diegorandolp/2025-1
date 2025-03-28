#!/usr/bin/env python3
import sys

def inp():
    return sys.stdin.readline().strip()


def get_int():
    return int(inp())


def get_ints():
    return list(map(int, inp().split()))


def main():
    """A"""
    # n = get_int()
    # numbers = get_ints()
    #
    # sum_ = sum(numbers)
    # missing = n * (n + 1) // 2 - sum_
    # print(missing)

    """B"""
    # n = get_int()
    # s = inp()
    #
    # s = s.lower()
    # letters = {}
    #
    # for letter in s:
    #     letters[letter] = 1
    # if len(letters) < 26:
    #     print('NO')
    # else:
    #     print('YES')

    """C"""
    # n = get_int()
    # numbers = get_ints()
    #
    # t1 = []
    # t2 = []
    # t3 = []
    #
    # for i in range(n):
    #     idx = i + 1
    #     if numbers[i] == 1:
    #         t1.append(idx)
    #     elif numbers[i] == 2:
    #         t2.append(idx)
    #     else:
    #         t3.append(idx)
    # n_teams = min(len(t1), len(t2), len(t3))
    # print(n_teams)
    # for i in range(n_teams):
    #     print(t1[i], t2[i], t3[i])

    """D"""
    # n = get_int()
    # numbers = ''
    #
    # for i in range(4):
    #     numbers = numbers + sys.stdin.readline()
    #
    # reg_numbs = [0 for i in range(10)]
    #
    # for i in numbers:
    #     if i.isdigit():
    #         reg_numbs[int(i)] += 1
    # max_num = max(reg_numbs)
    # if max_num > 2 * n:
    #     print('NO')
    # else:
    #     print('YES')

    """E"""
    # numbers = get_ints()
    # desired_nums = [1, 1, 2, 2, 2, 8]
    # for i in range(len(numbers)):
    #     print(desired_nums[i] - numbers[i], end=' ')

    """F"""
    # print('Hello World!')

    """G"""
    # s = inp()
    # print(f'Thank you, {s}, and farewell!')

    """H"""
    s = inp()

    print(s + 'O')
if __name__ == '__main__':
    main()