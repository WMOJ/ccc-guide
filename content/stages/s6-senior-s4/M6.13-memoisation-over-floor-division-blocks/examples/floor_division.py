import sys


def main() -> None:
    raw = sys.stdin.read()
    data = raw.split()
    if not data:
        return

    n = int(data[0])
    total = 0
    blocks = 0
    d = 1
    while d <= n:
        q = n // d
        last = n // q
        count = last - d + 1
        total += q * count
        blocks += 1
        d = last + 1

    print(total)
    print(blocks)


if __name__ == "__main__":
    main()
