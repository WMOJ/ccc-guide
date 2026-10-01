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

    for i in range(size - 1, 0, -1):
        tree[i] = merge(tree[2 * i], tree[2 * i + 1])

    print("size", size)
    print("tree", tree)


if __name__ == "__main__":
    main()
