import sys


def main() -> None:
    raw = sys.stdin.read()
    tokens = raw.split()
    if not tokens:
        return
    n = int(tokens[0])
    factor = n
    d = 2
    while d * d <= n:
        if n % d == 0:
            factor = d
            break
        d += 1
    is_prime = n >= 2 and factor == n
    print(factor)
    print(is_prime)


if __name__ == "__main__":
    main()
