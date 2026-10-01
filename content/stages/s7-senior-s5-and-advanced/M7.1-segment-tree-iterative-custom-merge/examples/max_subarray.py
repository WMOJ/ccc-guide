import sys

NEG = -10 ** 18
IDENTITY = (0, NEG, NEG, NEG)


def merge(a, b):
    # A node is (total, best_prefix, best_suffix, best_inside).
    total = a[0] + b[0]
    best_prefix = max(a[1], a[0] + b[1])
    best_suffix = max(b[2], b[0] + a[2])
    best_inside = max(a[3], b[3], a[2] + b[1])
    return (total, best_prefix, best_suffix, best_inside)


def main() -> None:
    data = sys.stdin.read().split()
    pos = 0
    n = int(data[pos])
    pos += 1

    size = 1
    while size < n:
        size *= 2

    tree = [IDENTITY] * (2 * size)
    for i in range(n):
        v = int(data[pos + i])
        tree[size + i] = (v, v, v, v)
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
            v = int(data[pos + 1])
            pos += 2
            tree[i] = (v, v, v, v)
            i //= 2
            while i >= 1:
                tree[i] = merge(tree[2 * i], tree[2 * i + 1])
                i //= 2
        else:
            lo = int(data[pos]) + size
            hi = int(data[pos + 1]) + size
            pos += 2
            left_part = IDENTITY
            right_part = IDENTITY
            while lo < hi:
                if lo % 2 == 1:
                    left_part = merge(left_part, tree[lo])
                    lo += 1
                if hi % 2 == 1:
                    hi -= 1
                    right_part = merge(tree[hi], right_part)
                lo //= 2
                hi //= 2
            answer = merge(left_part, right_part)
            results.append(answer[3])

    sys.stdout.write("\n".join(map(str, results)) + "\n")


if __name__ == "__main__":
    main()
