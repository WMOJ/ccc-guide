import sys


def main() -> None:
    data = sys.stdin.read().split()
    pos = 0
    rows = int(data[pos])
    cols = int(data[pos + 1])
    pos += 2
    grid = []
    for _ in range(rows):
        grid.append(data[pos:pos + cols])
        pos += cols

    result = [[grid[i][j] for i in range(rows)] for j in range(cols)]
    for row in result:
        print(" ".join(row))


if __name__ == "__main__":
    main()
