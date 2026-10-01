import sys


def main() -> None:
    data = sys.stdin.read().split()
    if not data:
        return

    n = int(data[0])

    counts = [0] * (n + 1)
    for d in range(1, n + 1):
        for multiple in range(d, n + 1, d):
            counts[multiple] += 1
    by_divisors = sum(counts)

    by_blocks = 0
    d = 1
    while d <= n:
        q = n // d
        last = n // q
        by_blocks += q * (last - d + 1)
        d = last + 1

    print(by_divisors)
    print(by_blocks)


if __name__ == "__main__":
    main()
