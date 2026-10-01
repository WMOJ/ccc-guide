import sys


def main() -> None:
    data = sys.stdin.read().split()
    pos = 0
    n = int(data[pos])
    pos += 1

    size = 1
    while size < n:
        size *= 2

    big = 10 ** 9
    tree = [big] * (2 * size)
    for i in range(n):
        tree[size + i] = int(data[pos + i])
    pos += n

    for i in range(size - 1, 0, -1):
        tree[i] = min(tree[2 * i], tree[2 * i + 1])

    q = int(data[pos])
    pos += 1

    results = []
    for _ in range(q):
        lo = int(data[pos]) + size
        hi = int(data[pos + 1]) + size
        pos += 2
        best = big
        while lo < hi:
            if lo % 2 == 1:
                best = min(best, tree[lo])
                lo += 1
            if hi % 2 == 1:
                hi -= 1
                best = min(best, tree[hi])
            lo //= 2
            hi //= 2
        results.append(best)

    sys.stdout.write("\n".join(map(str, results)) + "\n")


if __name__ == "__main__":
    main()
