import sys


def main() -> None:
    data = sys.stdin.read().split()
    n = int(data[0])

    row = [1]
    lines = []
    for _ in range(n + 1):
        lines.append(" ".join(map(str, row)))
        below = [1]
        for c in range(1, len(row)):
            below.append(row[c - 1] + row[c])
        below.append(1)
        row = below

    print("\n".join(lines))


if __name__ == "__main__":
    main()
