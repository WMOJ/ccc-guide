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

    last = 0
    results = []
    for _ in range(q):
        kind = int(data[pos])
        x = int(data[pos + 1])
        y = int(data[pos + 2])
        pos += 3

        if kind == 1:
            i = (x + last) % n + size
            tree[i] = (y + last) % 100
            i //= 2
            while i >= 1:
                tree[i] = merge(tree[2 * i], tree[2 * i + 1])
                i //= 2
        else:
            first = (x + last) % n
            second = (y + last) % n
            if first > second:
                first, second = second, first
            lo = first + size
            hi = second + 1 + size
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
            last = merge(left_part, right_part)
            results.append(last)

    sys.stdout.write("\n".join(map(str, results)) + "\n")


if __name__ == "__main__":
    main()
