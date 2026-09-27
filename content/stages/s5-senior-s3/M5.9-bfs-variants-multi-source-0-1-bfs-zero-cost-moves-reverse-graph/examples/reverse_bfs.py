from collections import deque

def reverse_bfs(adj, target):
    """BFS on reverse graph to compute distances to target."""
    n = len(adj)
    rev_adj = [[] for _ in range(n)]

    for u in range(n):
        for v in adj[u]:
            rev_adj[v].append(u)

    dist = [-1] * n
    dist[target] = 0
    queue = deque([target])

    while queue:
        u = queue.popleft()
        for v in rev_adj[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                queue.append(v)

    return dist


adj = [
    [1, 2],
    [3],
    [4],
    [5],
    [5],
    []
]

distances = reverse_bfs(adj, 5)
print("Distance from each node to target 5:", distances)
