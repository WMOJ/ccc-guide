import sys


def main() -> None:
    data = sys.stdin.read().split()
    r = int(data[0])
    c = int(data[1])
    grid = data[2:2 + r]

    count = 0
    for row in range(r):
        for col in range(c):
            if grid[row][col] == "#":
                count += 1

    print(count)


if __name__ == "__main__":
    main()
