import sys


def main() -> None:
    d = sys.stdin.read().split()
    n = int(d[0])
    vals = d[1:n + 1]
    a = list(map(int, vals))
    qs = d[n + 1:]
    last = 0
    for k in (0, 2):
        x = int(qs[k])
        y = int(qs[k + 1])
        lo = (x + last) % n
        hi = (y + last) % n
        if lo > hi:
            lo, hi = hi, lo
        seg = a[lo:hi + 1]
        last = sum(seg)
        print(last)


if __name__ == "__main__":
    main()
