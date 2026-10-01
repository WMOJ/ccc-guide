import sys


def main() -> None:
    data = sys.stdin.read().split()
    n = int(data[0])
    readings = list(map(int, data[1:1 + n]))

    counts = {}
    for value in readings:
        counts[value] = counts.get(value, 0) + 1

    pairs = 0
    for k in counts.values():
        pairs += k * (k - 1) // 2

    print(pairs)


if __name__ == "__main__":
    main()
