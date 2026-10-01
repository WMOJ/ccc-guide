import sys


def build_adjacency(n, edges):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    return adj


def dfs_preorder(adj, root):
    seen = [False] * len(adj)
    stack = [root]
    order = []

    while stack:
        node = stack.pop()
        if seen[node]:
            continue
        seen[node] = True
        order.append(node)
        for neighbor in reversed(adj[node]):
            if not seen[neighbor]:
                stack.append(neighbor)

    return order


def solve() -> None:
    data = sys.stdin.read().split()
    if not data:
        return
    pos = 0
    n = int(data[pos])
    m = int(data[pos + 1])
    pos += 2

    edges = []
    for _ in range(m):
        u = int(data[pos])
        v = int(data[pos + 1])
        pos += 2
        edges.append((u, v))

    adj = build_adjacency(n, edges)
    order = dfs_preorder(adj, 0)
    print("Preorder:", order)


def main() -> None:
    solve()


if __name__ == "__main__":
    main()
