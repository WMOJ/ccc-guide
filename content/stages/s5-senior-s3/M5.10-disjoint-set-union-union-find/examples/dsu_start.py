import sys


def find(parent: list, x: int) -> int:
    """Follow parent pointers to the root."""
    while parent[x] != x:
        x = parent[x]
    return x


def union(parent: list, a: int, b: int) -> None:
    """Merge the groups containing a and b."""
    root_a = find(parent, a)
    root_b = find(parent, b)
    if root_a != root_b:
        parent[root_a] = root_b


def main() -> None:
    data = sys.stdin.read().split()
    if not data:
        return

    n = int(data[0])
    m = int(data[1])
    parent = list(range(n))

    pos = 2
    for _ in range(m):
        a = int(data[pos])
        b = int(data[pos + 1])
        pos += 2
        union(parent, a, b)
        print(f"After union({a}, {b}):", parent)

    q = int(data[pos])
    pos += 1
    for _ in range(q):
        x = int(data[pos])
        pos += 1
        print(f"find({x}):", find(parent, x))


if __name__ == "__main__":
    main()
