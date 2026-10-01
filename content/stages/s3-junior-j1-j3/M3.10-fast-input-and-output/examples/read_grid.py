import sys


def main() -> None:
    tokens = sys.stdin.read().split()
    if not tokens:
        return

    idx = 0
    rows = int(tokens[idx])
    idx += 1
    cols = int(tokens[idx])
    idx += 1

    grid = []
    for r in range(rows):
        row = []
        for c in range(cols):
            row.append(int(tokens[idx]))
            idx += 1
        grid.append(row)

    total = 0
    for row in grid:
        for value in row:
            total += value

    sys.stdout.write(str(total) + "\n")


if __name__ == "__main__":
    main()
