import sys
from bisect import bisect_right


def main() -> None:
    data = sys.stdin.read().split()
    pos = 0
    n = int(data[pos])
    pos += 1
    days = sorted(map(int, data[pos:pos + n]))
    pos += n

    q = int(data[pos])
    pos += 1
    counts = []
    for _ in range(q):
        query_day = int(data[pos])
        pos += 1
        counts.append(bisect_right(days, query_day))

    print("\n".join(map(str, counts)))


if __name__ == "__main__":
    main()
