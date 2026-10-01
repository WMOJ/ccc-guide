import sys


def place(row, n, columns, diagonals_down, diagonals_up):
    if row == n:
        return 1
    total = 0
    for col in range(n):
        if col in columns:
            continue
        if (row - col) in diagonals_down:
            continue
        if (row + col) in diagonals_up:
            continue
        columns.add(col)
        diagonals_down.add(row - col)
        diagonals_up.add(row + col)
        total += place(row + 1, n, columns, diagonals_down, diagonals_up)
        columns.remove(col)
        diagonals_down.remove(row - col)
        diagonals_up.remove(row + col)
    return total


def solve() -> None:
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    n = int(input_data[0])
    print(place(0, n, set(), set(), set()))


def main() -> None:
    solve()


if __name__ == "__main__":
    main()
