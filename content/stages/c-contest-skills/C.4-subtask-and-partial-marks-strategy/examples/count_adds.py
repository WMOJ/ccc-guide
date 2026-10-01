import sys


def main() -> None:
    raw = sys.stdin.read()
    tokens = raw.split()
    k = int(tokens[0])
    for p in range(k):
        n = int(tokens[p + 1])
        cubic = n * (n + 1) * (n + 2) // 6
        quadratic = n * (n + 1) // 2
        print(f"n={n} cubic={cubic} quadratic={quadratic} linear={n}")


if __name__ == "__main__":
    main()
