import sys


def main() -> None:
    raw = sys.stdin.read()
    s = raw.rstrip("\n")
    n = len(s)
    concat_total = 0
    for k in range(1, n + 1):
        concat_total += k
    join_total = 2 * n
    print(concat_total, join_total)


if __name__ == "__main__":
    main()
