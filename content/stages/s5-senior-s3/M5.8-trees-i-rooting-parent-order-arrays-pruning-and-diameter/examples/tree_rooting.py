from collections import deque


def root_tree(adj, root):
    """Root a tree at a node, compute parent and depth."""
    n = len(adj)
    parent = [-1] * n
    depth = [-1] * n
    depth[root] = 0
    queue = deque([root])

    while queue:
        u = queue.popleft()
        for v in adj[u]:
            if depth[v] == -1:
                depth[v] = depth[u] + 1
                parent[v] = u
                queue.append(v)

    return parent, depth


adj = [
    [1, 2],
    [0, 3, 4],
    [0, 5],
    [1],
    [1],
    [2]
]

parent, depth = root_tree(adj, 0)
print("Parent:", parent)
print("Depth:", depth)
