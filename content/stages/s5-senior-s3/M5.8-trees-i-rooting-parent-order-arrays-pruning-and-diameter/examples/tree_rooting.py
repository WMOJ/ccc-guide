import sys
from collections import deque


def build_adjacency(n: int, edges: list) -> list:
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    return adj


def root_tree(adj: list, root: int) -> tuple:
    """Root a tree with an iterative BFS, filling parent, depth and the BFS order."""
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

    adj = build_adjacency(n, edges)
    parent, depth, order = root_tree(adj, root)
    print("Parent:", parent)
    print("Depth:", depth)
    print("Order:", order)


if __name__ == "__main__":
    main()
