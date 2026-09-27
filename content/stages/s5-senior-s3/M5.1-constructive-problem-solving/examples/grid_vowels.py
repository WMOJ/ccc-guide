import sys


def main() -> None:
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    m = int(input_data[1])

    if n == 0 or m == 0:
        return

    for i in range(n):
        row = "a" * m
        print(row)


if __name__ == "__main__":
    main()
