import sys


def main() -> None:
    input_data = sys.stdin.read().split()
    n = int(input_data[0])

    xs = []
    ys = []
    rects = []

    for i in range(n):
        x1 = int(input_data[1 + i * 4])
        y1 = int(input_data[1 + i * 4 + 1])
        x2 = int(input_data[1 + i * 4 + 2])
        y2 = int(input_data[1 + i * 4 + 3])
        rects.append((x1, y1, x2, y2))
        xs.extend([x1, x2])
        ys.extend([y1, y2])

    xs = sorted(set(xs))
    ys = sorted(set(ys))

    # Create difference array
    diff = [[0] * len(ys) for _ in range(len(xs))]

    # Add rectangles to difference array
    for x1, y1, x2, y2 in rects:
        xi1 = xs.index(x1)
        yi1 = ys.index(y1)
        xi2 = xs.index(x2)
        yi2 = ys.index(y2)

        diff[xi1][yi1] += 1
        diff[xi2][yi1] -= 1
        diff[xi1][yi2] -= 1
        diff[xi2][yi2] += 1

    # Compute 2D prefix sum
    area = 0
    for i in range(len(xs) - 1):
        for j in range(len(ys) - 1):
            if i > 0:
                diff[i][j] += diff[i - 1][j]
            if j > 0:
                diff[i][j] += diff[i][j - 1]
            if i > 0 and j > 0:
                diff[i][j] -= diff[i - 1][j - 1]

            if diff[i][j] > 0:
                width = xs[i + 1] - xs[i]
                height = ys[j + 1] - ys[j]
                area += width * height

    print(area)


if __name__ == "__main__":
    main()
