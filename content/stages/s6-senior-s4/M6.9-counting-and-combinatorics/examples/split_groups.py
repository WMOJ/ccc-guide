import math
import sys


def main() -> None:
    data = sys.stdin.read().split()
    k = int(data[0])
    sizes = list(map(int, data[1:1 + k]))

    left = sum(sizes)
    ways = 1
    for size in sizes:
        ways *= math.comb(left, size)
        left -= size

    print(ways)


if __name__ == "__main__":
    main()
