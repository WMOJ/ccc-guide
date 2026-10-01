import sys


def main() -> None:
    data = sys.stdin.read().split()
    pos = 0
    rows = int(data[pos])
    cols = int(data[pos + 1])
    pos += 2
    grid = []
    for _ in range(rows):
        grid.append([int(x) for x in data[pos:pos + cols]])
        pos += cols

    transposed = [[grid[i][j] for i in range(rows)] for j in range(cols)]
    result = [row[::-1] for row in transposed]
    for row in result:
        print(" ".join(map(str, row)))


if __name__ == "__main__":
    main()
