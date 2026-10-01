import sys


def main() -> None:
    data = sys.stdin.read().split()
    pos = 0
    n = int(data[pos])
    pos += 1
    a = [int(x) for x in data[pos:pos + n]]
    pos += n
    q = int(data[pos])
    pos += 1

    b = 1
    while b * b < n:
        b += 1
    tops = []
    for start in range(0, n, b):
        tops.append(max(a[start:start + b]))

    results = []
    for _ in range(q):
        kind = int(data[pos])
        x = int(data[pos + 1])
        y = int(data[pos + 2])
        pos += 3
        if kind == 1:
            a[x] = y
            start = x // b * b
            tops[x // b] = max(a[start:start + b])
        else:
            lo = x
            hi = y
            best = a[lo]
            while lo < hi and lo % b != 0:
                best = max(best, a[lo])
                lo += 1
            while lo + b <= hi:
                best = max(best, tops[lo // b])
                lo += b
            while lo < hi:
                best = max(best, a[lo])
                lo += 1
            results.append(best)

    sys.stdout.write("\n".join(map(str, results)) + "\n")


if __name__ == "__main__":
    main()
