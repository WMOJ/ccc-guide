import sys


def find(parent: list, x: int) -> int:
    """Find root with path halving."""
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x


def union(parent: list, size: list, a: int, b: int) -> bool:
    """Merge groups containing a and b; False if they were already one group."""
    root_a = find(parent, a)
    root_b = find(parent, b)
    if root_a == root_b:
        return False
    if size[root_a] < size[root_b]:
        parent[root_a] = root_b
        size[root_b] += size[root_a]
    else:
        parent[root_b] = root_a
        size[root_a] += size[root_b]
    return True


def main() -> None:
    data = sys.stdin.read().split()
    if not data:
        return

    n = int(data[0])
    m = int(data[1])
    edges = []
    pos = 2
    for _ in range(m):
        u = int(data[pos])
        v = int(data[pos + 1])
        w = int(data[pos + 2])
        pos += 3
        edges.append((w, u, v))
    edges.sort()

    parent = list(range(n))
    size = [1] * n
    total = 0
    chosen = []
    for w, u, v in edges:
        if union(parent, size, u, v):
            total += w
            chosen.append(f"{u}-{v}")
            if len(chosen) == n - 1:
                break

    if len(chosen) == n - 1:
        print(total)
        print(" ".join(chosen))
    else:
        print(-1)


if __name__ == "__main__":
    main()
