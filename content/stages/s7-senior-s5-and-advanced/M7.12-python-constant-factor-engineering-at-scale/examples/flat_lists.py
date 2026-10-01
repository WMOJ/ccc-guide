import sys


def main() -> None:
    raw = sys.stdin.read()
    tokens = raw.split()
    n = int(tokens[0])
    points = []
    xs = []
    ys = []
    pos = 1
    for _ in range(n):
        x = int(tokens[pos])
        y = int(tokens[pos + 1])
        pos += 2
        points.append((x, y))
        xs.append(x)
        ys.append(y)

    by_tuples = 0
    for x, y in points:
        by_tuples += x * y
    by_lists = 0
    for i in range(n):
        by_lists += xs[i] * ys[i]
    print(by_tuples, by_lists)


if __name__ == "__main__":
    main()
