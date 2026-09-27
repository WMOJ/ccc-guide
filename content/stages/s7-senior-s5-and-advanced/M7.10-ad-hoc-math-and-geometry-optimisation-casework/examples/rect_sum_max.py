import sys


def main() -> None:
    input_data = sys.stdin.read().split()
    n = int(input_data[0])
    k = int(input_data[1])
    grid = []
    idx = 2
    for i in range(n):
        row = [int(input_data[idx + j]) for j in range(n)]
        grid.append(row)
        idx += n

    # Build 2D prefix sum
    prefix = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            prefix[i][j] = grid[i - 1][j - 1] + prefix[i - 1][j] + prefix[i][j - 1] - prefix[i - 1][j - 1]

    # Find max sum of k by k rectangle. Seed with the first candidate, not 0,
    # so a grid of entirely negative values still gives the right answer.
    max_sum = None
    for i in range(k, n + 1):
        for j in range(k, n + 1):
            rect_sum = prefix[i][j] - prefix[i - k][j] - prefix[i][j - k] + prefix[i - k][j - k]
            if max_sum is None or rect_sum > max_sum:
                max_sum = rect_sum

    print(max_sum)


if __name__ == "__main__":
    main()
