import sys


def main() -> None:
    input_data = sys.stdin.read().split()
    n = int(input_data[0])
    grid = []
    idx = 1
    for i in range(n):
        row = [int(input_data[idx + j]) for j in range(n)]
        grid.append(row)
        idx += n

    # Build sparse table for 2D range max
    # table[i][j][k][l] = max over rectangle starting at (i,j) of size 2^k by 2^l
    table = [[[[0 for _ in range(10)] for _ in range(10)] for _ in range(n)] for _ in range(n)]

    # Base case: 2^0 by 2^0 (single cell)
    for i in range(n):
        for j in range(n):
            table[i][j][0][0] = grid[i][j]

    # Fill for increasing powers
    for k in range(1, 10):
        for i in range(n):
            for j in range(n):
                if i + (1 << k) > n or j + (1 << k) > n:
                    continue
                # Max of four 2^(k-1) by 2^(k-1) rectangles
                half = 1 << (k - 1)
                val = max(
                    table[i][j][k - 1][k - 1],
                    table[i + half][j][k - 1][k - 1],
                    table[i][j + half][k - 1][k - 1],
                    table[i + half][j + half][k - 1][k - 1]
                )
                table[i][j][k][k] = val

    # Query: max in rectangle from (0,0) to (n-1,n-1)
    result = table[0][0][9][9] if n <= 512 else max(table[i][j][9][9] for i in range(n) for j in range(n) if i + 512 <= n and j + 512 <= n)
    print(result)


if __name__ == "__main__":
    main()
