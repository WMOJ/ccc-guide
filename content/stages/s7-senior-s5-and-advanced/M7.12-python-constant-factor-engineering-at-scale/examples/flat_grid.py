import sys


def main() -> None:
    raw = sys.stdin.read()
    tokens = raw.split()
    rows = int(tokens[0])
    cols = int(tokens[1])
    cells = []
    for k in range(rows * cols):
        cells.append(int(tokens[2 + k]))
    r = int(tokens[2 + rows * cols])
    c = int(tokens[3 + rows * cols])

    here = r * cols + c
    right = "none"
    if c + 1 < cols:
        right = str(cells[here + 1])
    down = "none"
    if r + 1 < rows:
        down = str(cells[here + cols])
    print(f"cell {cells[here]} right {right} down {down}")


if __name__ == "__main__":
    main()
