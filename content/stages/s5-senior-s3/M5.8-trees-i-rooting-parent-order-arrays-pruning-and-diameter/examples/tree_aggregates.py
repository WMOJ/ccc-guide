def compute_subtree_aggregates(adj, root):
    """Compute subtree size and max depth using postorder DFS."""
    n = len(adj)
    subtree_size = [0] * n
    max_depth = [0] * n
    visited = [False] * n

    def dfs(u):
        visited[u] = True
        subtree_size[u] = 1
        max_depth[u] = 0

        for v in adj[u]:
            if not visited[v]:
                dfs(v)
                subtree_size[u] += subtree_size[v]
                max_depth[u] = max(max_depth[u], max_depth[v] + 1)

    dfs(root)
    return subtree_size, max_depth


adj = [
    [1, 2],
    [0, 3, 4],
    [0, 5],
    [1],
    [1],
    [2]
]

size, depth = compute_subtree_aggregates(adj, 0)
print("Subtree sizes:", size)
print("Max depths:", depth)
