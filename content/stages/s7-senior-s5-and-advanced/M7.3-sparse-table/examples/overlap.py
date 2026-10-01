import sys
from functools import reduce
from math import gcd
from operator import add


def main() -> None:
    data = sys.stdin.read().split()
    name = data[0]
    n = int(data[1])
    a = []
    pos = 2
    for _ in range(n):
        a.append(int(data[pos]))
        pos += 1
    left = int(data[pos])
    last = int(data[pos + 1])

    ops = {"min": min, "gcd": gcd, "sum": add}
    op = ops[name]

    size = 1
    while size * 2 <= last - left + 1:
        size *= 2
    first = reduce(op, a[left:left + size])
    second = reduce(op, a[last - size + 1:last + 1])
    two_blocks = op(first, second)
    truth = reduce(op, a[left:last + 1])
    print(f"two blocks: {two_blocks}, true answer: {truth}")


if __name__ == "__main__":
    main()
