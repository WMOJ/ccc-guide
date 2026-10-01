import sys


def main() -> None:
    raw = sys.stdin.read()
    tokens = raw.split()
    a = int(tokens[0])
    b = int(tokens[1])
    m = int(tokens[2])
    r = 1
    while b > 0:
        if b % 2 == 1:
            r = r * a % m
        a = a * a % m
        b //= 2
    print(r)


if __name__ == "__main__":
    main()
