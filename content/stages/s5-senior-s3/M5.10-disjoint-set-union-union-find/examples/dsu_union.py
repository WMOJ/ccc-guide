import sys


def find(parent: list, x: int) -> int:
    """Find root with path halving."""
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x


def union(parent: list, size: list, a: int, b: int) -> None:
    """Merge groups containing a and b; attach smaller tree under larger."""
    root_a = find(parent, a)
    root_b = find(parent, b)
    if root_a == root_b:
        return
    if size[root_a] < size[root_b]:
        parent[root_a] = root_b
        size[root_b] += size[root_a]
    else:
        parent[root_b] = root_a
        size[root_a] += size[root_b]


def main() -> None:
    data = sys.stdin.read().split()
    if not data:
        return

    n = int(data[0])
    m = int(data[1])
    parent = list(range(n))
    size = [1] * n

    pos = 2
    for _ in range(m):
        a = int(data[pos])
        b = int(data[pos + 1])
        pos += 2
        union(parent, size, a, b)
        print(f"After union({a}, {b}):", parent)

    print("Sizes:", size)


if __name__ == "__main__":
    main()
