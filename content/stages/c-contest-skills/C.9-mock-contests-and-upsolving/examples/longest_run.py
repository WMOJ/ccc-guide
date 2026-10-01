import sys


def main() -> None:
    raw = sys.stdin.read()
    t = raw.split()
    a = list(map(int, t))
    best = 1
    run = 1
    for i in range(1, len(a)):
        if a[i] > a[i - 1]:
            run += 1
        else:
            run = 0
        best = max(best, run)
    print(best)


if __name__ == "__main__":
    main()
