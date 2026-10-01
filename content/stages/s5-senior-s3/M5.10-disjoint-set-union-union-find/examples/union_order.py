import sys


def find(parent: list, x: int) -> int:
    """Follow parent pointers to the root, with no halving so the shape stays visible."""
    while parent[x] != x:
        x = parent[x]
    return x


def height(parent: list) -> int:
    """The most hops any element needs to reach its root."""
    worst = 0
    for start in range(len(parent)):
        x = start
        hops = 0
        while parent[x] != x:
            x = parent[x]
            hops += 1
        worst = max(worst, hops)
    return worst


def main() -> None:
    data = sys.stdin.read().split()
    if not data:
        return

    n = int(data[0])
    m = int(data[1])
    naive = list(range(n))
    by_size = list(range(n))
    size = [1] * n

    pos = 2
    for _ in range(m):
        a = int(data[pos])
        b = int(data[pos + 1])
        pos += 2

        # Naive: the first root always goes under the second.
        root_a = find(naive, a)
        root_b = find(naive, b)
        if root_a != root_b:
            naive[root_a] = root_b

        # By size: the smaller tree goes under the larger.
        root_a = find(by_size, a)
        root_b = find(by_size, b)
        if root_a != root_b:
            if size[root_a] < size[root_b]:
                by_size[root_a] = root_b
                size[root_b] += size[root_a]
            else:
                by_size[root_b] = root_a
                size[root_a] += size[root_b]

    print("Naive:", naive, "height", height(naive))
    print("By size:", by_size, "height", height(by_size))


if __name__ == "__main__":
    main()
