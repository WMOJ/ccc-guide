import sys


def main() -> None:
    raw = sys.stdin.read()
    d = raw.split()
    target = int(d[-1])
    a = list(map(int, d[1:-1]))
    best = {0: 0}
    prefix = 0
    dp = 0
    for x in a:
        prefix += x - target
        if prefix in best:
            dp = max(dp, best[prefix] + 1)
        best[prefix] = dp
    print(dp)


if __name__ == "__main__":
    main()
