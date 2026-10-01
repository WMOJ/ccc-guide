import sys


def main() -> None:
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    idx = 0
    rows, cols = int(input_data[idx]), int(input_data[idx + 1])
    idx += 2
    grid = []
    for _ in range(rows):
        grid.append([int(x) for x in input_data[idx:idx + cols]])
        idx += cols

    # Build 2D prefix sum
    prefix = [[0] * (cols + 1) for _ in range(rows + 1)]
    for r in range(rows):
        row = grid[r]
        prev_row = prefix[r]
        cur_row = prefix[r + 1]
        for c in range(cols):
            cur_row[c + 1] = row[c] + prev_row[c + 1] + cur_row[c] - prev_row[c]

    # Answer rectangle queries
    q = int(input_data[idx])
    idx += 1
    out_lines = []
    for _ in range(q):
        r1, c1, r2, c2 = (int(v) for v in input_data[idx:idx + 4])
        idx += 4
        rect_sum = (
            prefix[r2 + 1][c2 + 1]
            - prefix[r1][c2 + 1]
            - prefix[r2 + 1][c1]
            + prefix[r1][c1]
        )
        out_lines.append(str(rect_sum))
    sys.stdout.write("\n".join(out_lines) + "\n")


if __name__ == "__main__":
    main()
