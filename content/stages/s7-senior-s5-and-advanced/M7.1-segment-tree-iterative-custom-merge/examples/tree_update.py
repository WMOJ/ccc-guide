import sys


def merge(a, b):
    return a + b


def main() -> None:
    data = sys.stdin.read().split()
    pos = 0
    n = int(data[pos])
    pos += 1

    size = 1
    while size < n:
        size *= 2

    tree = [0] * (2 * size)
    for i in range(n):
        tree[size + i] = int(data[pos + i])
    pos += n

    for i in range(size - 1, 0, -1):
        tree[i] = merge(tree[2 * i], tree[2 * i + 1])

    q = int(data[pos])
    pos += 1

    results = []
    for _ in range(q):
        kind = int(data[pos])
        pos += 1

        if kind == 1:
            i = int(data[pos]) + size
            tree[i] = int(data[pos + 1])
            pos += 2
            i //= 2
            while i >= 1:
                tree[i] = merge(tree[2 * i], tree[2 * i + 1])
                i //= 2
        else:
            lo = int(data[pos]) + size
            hi = int(data[pos + 1]) + size
            pos += 2
            left_part = 0
            right_part = 0
            while lo < hi:
                if lo % 2 == 1:
                    left_part = merge(left_part, tree[lo])
                    lo += 1
                if hi % 2 == 1:
                    hi -= 1
                    right_part = merge(tree[hi], right_part)
                lo //= 2
                hi //= 2
            results.append(merge(left_part, right_part))

    sys.stdout.write("\n".join(map(str, results)) + "\n")


if __name__ == "__main__":
    main()
