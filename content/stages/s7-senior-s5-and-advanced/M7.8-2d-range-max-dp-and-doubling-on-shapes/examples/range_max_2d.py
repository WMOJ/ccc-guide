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

    # table[k] holds the sparse table for 2^k by 2^k squares.
    # table[k][i][j] is the max over rows i..i+2^k-1 and columns j..j+2^k-1.
    max_k = 0
    while (1 << (max_k + 1)) <= n:
        max_k += 1

    table = [grid]
    for k in range(1, max_k + 1):
        half = 1 << (k - 1)
        prev = table[k - 1]
        span = len(prev) - half
        layer = []
        for i in range(span):
            row = []
            for j in range(span):
                row.append(max(
                    prev[i][j],
                    prev[i + half][j],
                    prev[i][j + half],
                    prev[i + half][j + half],
                ))
            layer.append(row)
        table.append(layer)

    def query(r1, c1, r2, c2):
        # Decompose the square region into two overlapping power-of-2 squares
        # per side and take the max of the four corners.
        side = r2 - r1 + 1
        k = side.bit_length() - 1
        size = 1 << k
        t = table[k]
        return max(
            t[r1][c1],
            t[r2 - size + 1][c1],
            t[r1][c2 - size + 1],
            t[r2 - size + 1][c2 - size + 1],
        )

    print(query(0, 0, n - 1, n - 1))


if __name__ == "__main__":
    main()
