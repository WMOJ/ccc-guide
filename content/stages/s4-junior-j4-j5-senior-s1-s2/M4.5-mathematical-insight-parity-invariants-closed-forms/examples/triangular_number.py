import sys


def main() -> None:
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])

    # A loop would add n numbers one at a time. The closed form skips
    # straight to the total.
    total = n * (n + 1) // 2

    sys.stdout.write(str(total) + "\n")


if __name__ == "__main__":
    main()
