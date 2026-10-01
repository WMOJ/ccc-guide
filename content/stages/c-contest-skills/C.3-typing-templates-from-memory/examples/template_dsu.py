import sys


def main() -> None:
    data = sys.stdin.read().split()
    if not data:
        return

    n = int(data[0])
    m = int(data[1])
    parent = list(range(n))
    size = [1] * n

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a: int, b: int) -> None:
        root_a = find(a)
        root_b = find(b)
        if root_a == root_b:
            return
        if size[root_a] < size[root_b]:
            parent[root_a] = root_b
            size[root_b] += size[root_a]
        else:
            parent[root_b] = root_a
            size[root_a] += size[root_b]

    pos = 2
    for _ in range(m):
        u = int(data[pos])
        v = int(data[pos + 1])
        pos += 2
        union(u, v)

    q = int(data[pos])
    pos += 1
    out_lines = []
    for _ in range(q):
        a = int(data[pos])
        b = int(data[pos + 1])
        pos += 2
        out_lines.append("yes" if find(a) == find(b) else "no")

    print("\n".join(out_lines))


if __name__ == "__main__":
    main()
