import sys


def solve() -> None:
    data = sys.stdin.read().split()
    pos = 0
    r = int(data[pos])
    c = int(data[pos + 1])
    pos += 2
    grid = []
    for _ in range(r):
        grid.append([int(x) for x in data[pos:pos + c]])
        pos += c

    for row in grid:
        print(sum(row))

    col_sums = []
    for col in range(c):
        total = 0
        for row in range(r):
            total += grid[row][col]
        col_sums.append(total)
    print(*col_sums)


def main() -> None:
    solve()


if __name__ == "__main__":
    main()
