import sys
from collections import deque


def build_adjacency(n: int, edges: list) -> list:
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    return adj


def root_tree(adj: list, root: int) -> tuple:
    n = len(adj)
    parent = [-1] * n
    depth = [-1] * n
    order = []
    depth[root] = 0
    queue = deque([root])
    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in adj[node]:
            if depth[neighbor] == -1:
                depth[neighbor] = depth[node] + 1
                parent[neighbor] = node
                queue.append(neighbor)
    return parent, depth, order


def subtree_aggregates(adj: list, root: int, items: list) -> tuple:
    """Subtree room count and item total, added into each parent as order runs in reverse."""
    parent, _depth, order = root_tree(adj, root)
    size = [1] * len(adj)
    total = list(items)
    for node in reversed(order):
        above = parent[node]
        if above != -1:
            size[above] += size[node]
            total[above] += total[node]
    return size, total


def main() -> None:
    data = sys.stdin.read().split()
    if not data:
        return

    pos = 0
    n = int(data[pos])
    root = int(data[pos + 1])
    pos += 2

    edges = []
    for _ in range(n - 1):
        a = int(data[pos])
        b = int(data[pos + 1])
        pos += 2
        edges.append((a, b))

    items = []
    for _ in range(n):
        items.append(int(data[pos]))
        pos += 1

    adj = build_adjacency(n, edges)
    size, total = subtree_aggregates(adj, root, items)
    print("Room count:", size)
    print("Item total:", total)


if __name__ == "__main__":
    main()
