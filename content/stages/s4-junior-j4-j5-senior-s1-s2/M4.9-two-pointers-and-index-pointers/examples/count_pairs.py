"""Counting variant: how many pairs in a sorted list sum to at most K."""

import sys


def solve() -> None:
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    k = int(input_data[1])
    arr = [int(x) for x in input_data[2 : n + 2]]

    left = 0
    right = n - 1
    count = 0
    while left < right:
        if arr[left] + arr[right] <= k:
            count += right - left
            left += 1
        else:
            right -= 1

    print(count)


def main() -> None:
    solve()


if __name__ == "__main__":
    main()
