import sys


def main() -> None:
    data = sys.stdin.read().split()
    n = int(data[0])
    pos = 1
    xs = set()
    ys = set()
    rects = []
    for _ in range(n):
        x1 = int(data[pos])
        y1 = int(data[pos + 1])
        x2 = int(data[pos + 2])
        y2 = int(data[pos + 3])
        pos += 4
        rects.append((x1, y1, x2, y2))
        xs.add(x1)
        xs.add(x2)
        ys.add(y1)
        ys.add(y2)

    xs = sorted(xs)
    ys = sorted(ys)
    x_rank = {x: i for i, x in enumerate(xs)}
    y_rank = {y: i for i, y in enumerate(ys)}

    widths = [xs[i + 1] - xs[i] for i in range(len(xs) - 1)]
    heights = [ys[j + 1] - ys[j] for j in range(len(ys) - 1)]
    print("widths", widths)
    print("heights", heights)
    for x1, y1, x2, y2 in rects:
        print("columns", x_rank[x1], "to", x_rank[x2], "rows", y_rank[y1], "to", y_rank[y2])


if __name__ == "__main__":
    main()
