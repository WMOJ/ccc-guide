import sys


def digital_root(n):
    while n >= 10:
        total = 0
        while n > 0:
            total += n % 10
            n //= 10
        n = total
    return n


def main() -> None:
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    start = int(input_data[0])
    values = []
    for n in range(start, start + 6):
        values.append(str(digital_root(n)))
    print(" ".join(values))


if __name__ == "__main__":
    main()
