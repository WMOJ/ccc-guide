import sys
from math import isqrt


def main() -> None:
    data = sys.stdin.read().split()
    if not data:
        return

    limit = int(data[0])
    distinct = []
    for n in range(1, limit + 1):
        values = set()
        for d in range(1, n + 1):
            values.add(n // d)
        distinct.append(len(values))

    print(distinct[-1])
    print(2 * isqrt(limit))


if __name__ == "__main__":
    main()
