import sys
from random import randint, seed


def main() -> None:
    raw = sys.stdin.read()
    tokens = raw.split()
    start = int(tokens[0])
    count = int(tokens[1])

    seed(start)
    first = []
    for _ in range(count):
        x = randint(1, 99)
        first.append(x)

    seed(start)
    second = []
    for _ in range(count):
        x = randint(1, 99)
        second.append(x)

    print(*first)
    print(*second)
    print(first == second)


if __name__ == "__main__":
    main()
