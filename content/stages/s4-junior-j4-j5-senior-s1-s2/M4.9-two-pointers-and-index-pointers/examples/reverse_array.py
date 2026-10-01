"""Pointers closing in from both ends: reverse a list in place."""

import sys


def solve() -> None:
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    arr = [int(x) for x in input_data[1 : n + 1]]

    left = 0
    right = n - 1
    while left < right:
        arr[left], arr[right] = arr[right], arr[left]
        left += 1
        right -= 1

    print(" ".join(str(x) for x in arr))


def main() -> None:
    solve()


if __name__ == "__main__":
    main()
