import sys


def main() -> None:
    raw = sys.stdin.read()
    tokens = raw.split()
    n = int(tokens[0])
    values = list(map(int, tokens[1:]))
    best = 1
    run = 1
    for i in range(1, n):
        if values[i] == values[i - 1]:
            run += 1
        else:
            best = max(best, run)
            run = 1
    print(best)


if __name__ == "__main__":
    main()
