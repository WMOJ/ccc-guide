import sys


def main() -> None:
    data = sys.stdin.read().split()
    if not data:
        return

    pos = 0
    n = int(data[pos])
    pos += 1

    phone_numbers = {}
    for _ in range(n):
        name = data[pos]
        number = data[pos + 1]
        pos += 2
        phone_numbers[name] = number

    query = data[pos]
    pos += 1
    sys.stdout.write(f"{phone_numbers[query]}\n")


if __name__ == "__main__":
    main()
