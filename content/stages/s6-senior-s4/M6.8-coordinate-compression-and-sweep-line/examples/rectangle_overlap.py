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

    diff = [[0] * len(xs) for _ in range(len(ys))]
    for x1, y1, x2, y2 in rects:
        left = x_rank[x1]
        right = x_rank[x2]
        top = y_rank[y1]
        bottom = y_rank[y2]
        diff[top][left] += 1
        diff[top][right] -= 1
        diff[bottom][left] -= 1
        diff[bottom][right] += 1

    at_least_one = 0
    at_least_two = 0
    for j in range(len(ys) - 1):
        for i in range(len(xs) - 1):
            if j > 0:
                diff[j][i] += diff[j - 1][i]
            if i > 0:
                diff[j][i] += diff[j][i - 1]
            if i > 0 and j > 0:
                diff[j][i] -= diff[j - 1][i - 1]
            area = (xs[i + 1] - xs[i]) * (ys[j + 1] - ys[j])
            if diff[j][i] >= 1:
                at_least_one += area
            if diff[j][i] >= 2:
                at_least_two += area

    print(at_least_one)
    print(at_least_two)


if __name__ == "__main__":
    main()
