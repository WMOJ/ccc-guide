import sys
from bisect import bisect_left, bisect_right


def main() -> None:
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    pos = 0
    n = int(input_data[pos])
    pos += 1
    arr = [int(x) for x in input_data[pos : pos + n]]
    pos += n
    q = int(input_data[pos])
    pos += 1
    queries = [int(x) for x in input_data[pos : pos + q]]
    pos += q

    for x in queries:
        left = bisect_left(arr, x)
        right = bisect_right(arr, x)
        count = right - left
        print(f"{x}: left={left} right={right} count={count}")


if __name__ == "__main__":
    main()
