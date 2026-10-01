import sys


def main() -> None:
    data = sys.stdin.read().split()
    pos = 0
    n = int(data[pos])
    pos += 1
    values = list(map(int, data[pos:pos + n]))
    pos += n

    unique_values = sorted(set(values))
    rank = {value: i for i, value in enumerate(unique_values)}

    compressed = [rank[value] for value in values]
    print(" ".join(map(str, compressed)))


if __name__ == "__main__":
    main()
