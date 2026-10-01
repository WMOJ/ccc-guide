import sys


def main() -> None:
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    m = int(input_data[1])

    if n % 2 != 0 or m % 2 != 0:
        print("Impossible")
        return

    lines = []
    for r in range(n):
        row_chars = []
        for c in range(m):
            if (r + c) % 2 == 0:
                row_chars.append("a")
            else:
                row_chars.append("b")
        lines.append("".join(row_chars))
    print("\n".join(lines))


if __name__ == "__main__":
    main()
