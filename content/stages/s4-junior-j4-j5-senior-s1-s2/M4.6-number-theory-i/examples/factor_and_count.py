import sys


def main() -> None:
    raw = sys.stdin.read()
    tokens = raw.split()
    if not tokens:
        return
    n = int(tokens[0])
    remaining = n
    count = 1
    factors = []
    p = 2
    while p * p <= remaining:
        if remaining % p == 0:
            exponent = 0
            while remaining % p == 0:
                remaining //= p
                exponent += 1
            factors.append((p, exponent))
            count *= exponent + 1
        p += 1
    if remaining > 1:
        factors.append((remaining, 1))
        count *= 2
    parts = []
    for prime, exponent in factors:
        parts.append(f"{prime}^{exponent}")
    print(" ".join(parts))
    print(count)


if __name__ == "__main__":
    main()
