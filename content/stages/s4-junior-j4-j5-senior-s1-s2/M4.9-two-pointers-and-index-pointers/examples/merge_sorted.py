"""Index pointers: merge two sorted lists into one sorted list."""

import sys


def solve() -> None:
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    pos = 0
    n = int(input_data[pos])
    pos += 1
    a = [int(x) for x in input_data[pos : pos + n]]
    pos += n
    m = int(input_data[pos])
    pos += 1
    b = [int(x) for x in input_data[pos : pos + m]]

    merged = []
    i = 0
    j = 0
    while i < n and j < m:
        if a[i] <= b[j]:
            merged.append(a[i])
            i += 1
        else:
            merged.append(b[j])
            j += 1

    merged.extend(a[i:])
    merged.extend(b[j:])

    print(" ".join(str(x) for x in merged))


def main() -> None:
    solve()


if __name__ == "__main__":
    main()
