import sys


def main() -> None:
    raw = sys.stdin.read()
    data = raw.split()
    n = int(data[0])
    k = int(data[1])
    grid = []
    pos = 2
    for r in range(n):
        row = []
        for c in range(n):
            row.append(int(data[pos]))
            pos += 1
        grid.append(row)

    prefix = [[0] * (n + 1) for _ in range(n + 1)]
    for r in range(1, n + 1):
        for c in range(1, n + 1):
            above = prefix[r - 1][c]
            left = prefix[r][c - 1]
            both = prefix[r - 1][c - 1]
            prefix[r][c] = grid[r - 1][c - 1] + above + left - both

    best = None
    best_at = (0, 0)
    for r in range(k, n + 1):
        for c in range(k, n + 1):
            total = prefix[r][c] - prefix[r - k][c]
            total -= prefix[r][c - k] - prefix[r - k][c - k]
            if best is None or total > best:
                best = total
                best_at = (r - k, c - k)

    print(best)
    print(best_at[0], best_at[1])


if __name__ == "__main__":
    main()
