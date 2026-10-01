import sys


def find(parent: list, x: int) -> int:
    """Find root with path halving."""
    while parent[x] != x:
        parent[x] = parent[parent[x]]  # Skip one level
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

    print("Parent array after naive unions:", parent)

    x = int(data[pos])
    pos += 1
    print(f"find({x}) with path halving:", find(parent, x))
    print("Parent array after find:", parent)


if __name__ == "__main__":
    main()
