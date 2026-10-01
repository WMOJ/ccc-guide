import sys


def main() -> None:
    raw = sys.stdin.read()
    tokens = raw.split()
    n = int(tokens[0])
    squares = []
    add = squares.append
    for i in range(1, n + 1):
        x = int(tokens[i])
        add(x * x)
    print(*squares)


if __name__ == "__main__":
    main()
