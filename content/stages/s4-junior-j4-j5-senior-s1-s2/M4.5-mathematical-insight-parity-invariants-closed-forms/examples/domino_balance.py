import sys


def main() -> None:
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    cut = int(input_data[1])

    # Every domino covers one square with (row + col) % 2 == 0 and one with 1,
    # so a tiling needs the two counts to match. Count both, skipping the two
    # opposite corners when the board is cut.
    zeros = 0
    ones = 0
    for row in range(n):
        for col in range(n):
            if cut == 1 and row == col and (row == 0 or row == n - 1):
                continue
            if (row + col) % 2 == 0:
                zeros += 1
            else:
                ones += 1

    sys.stdout.write(f"{zeros} {ones}\n")
    if zeros == ones:
        sys.stdout.write("balanced\n")
    else:
        sys.stdout.write("no tiling\n")


if __name__ == "__main__":
    main()
