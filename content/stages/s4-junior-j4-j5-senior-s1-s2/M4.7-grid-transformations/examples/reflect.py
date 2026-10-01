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

    print("Original:")
    for row in grid:
        print(" ".join(row))

    print("\nHorizontal reflection:")
    h_result = [row[::-1] for row in grid]
    for row in h_result:
        print(" ".join(row))

    print("\nVertical reflection:")
    v_result = grid[::-1]
    for row in v_result:
        print(" ".join(row))


if __name__ == "__main__":
    main()
