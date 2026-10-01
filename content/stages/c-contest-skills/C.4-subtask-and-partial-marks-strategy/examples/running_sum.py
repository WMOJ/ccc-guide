import sys


def brute(values):
    n = len(values)
    best = values[0]
    for i in range(n):
        total = 0
        for j in range(i, n):
            total += values[j]
            best = max(best, total)
    return best


def main() -> None:
    raw = sys.stdin.read()
    tokens = raw.split()
    n = int(tokens[0])
    nums = tokens[1:n + 1]
    values = list(map(int, nums))
    print(brute(values))


if __name__ == "__main__":
    main()
