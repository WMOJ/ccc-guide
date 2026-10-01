"""Read/write pointers: collapse a sorted list down to its unique values, in place."""

import sys


def solve() -> None:
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    arr = [int(x) for x in input_data[1 : n + 1]]

    if n == 0:
        print()
        return

    write = 0
    for read in range(1, n):
        if arr[read] != arr[write]:
            write += 1
            arr[write] = arr[read]

    unique = arr[: write + 1]
    print(" ".join(str(x) for x in unique))


def main() -> None:
    solve()


if __name__ == "__main__":
    main()
