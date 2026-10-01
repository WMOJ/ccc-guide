import sys


def main() -> None:
    d = sys.stdin.read().split()
    lo = int(d[0])
    hi = int(d[1])
    a = list(map(int, d[2:]))
    n = len(a)
    b = 3
    sums = []
    for s in range(0, n, b):
        part = a[s:s + b]
        sums.append(sum(part))
    total = 0
    while lo < hi and lo % b:
        total += a[lo]
        lo += 1
    while lo + b <= hi:
        total += sums[lo // b]
        lo += b
    while lo < hi:
        total += a[lo]
        lo += 1
    print(total)


if __name__ == "__main__":
    main()
