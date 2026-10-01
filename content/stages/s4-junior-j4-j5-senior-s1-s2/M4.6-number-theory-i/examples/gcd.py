import sys


def main() -> None:
    raw = sys.stdin.read()
    tokens = raw.split()
    if not tokens:
        return
    a = int(tokens[0])
    b = int(tokens[1])
    x = a
    y = b
    while y != 0:
        x, y = y, x % y
    g = x
    lcm = a * b // g
    print(g)
    print(lcm)


if __name__ == "__main__":
    main()
