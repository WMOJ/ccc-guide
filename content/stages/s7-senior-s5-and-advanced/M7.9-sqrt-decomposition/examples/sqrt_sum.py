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
    sums = [0] * ((n + b - 1) // b)
    for i in range(n):
        sums[i // b] += a[i]

    results = []
    for _ in range(q):
        kind = int(data[pos])
        x = int(data[pos + 1])
        y = int(data[pos + 2])
        pos += 3
        if kind == 1:
            sums[x // b] += y - a[x]
            a[x] = y
        else:
            lo = x
            hi = y
            total = 0
            while lo < hi and lo % b != 0:
                total += a[lo]
                lo += 1
            while lo + b <= hi:
                total += sums[lo // b]
                lo += b
            while lo < hi:
                total += a[lo]
                lo += 1
            results.append(total)

    sys.stdout.write("\n".join(map(str, results)) + "\n")


if __name__ == "__main__":
    main()
