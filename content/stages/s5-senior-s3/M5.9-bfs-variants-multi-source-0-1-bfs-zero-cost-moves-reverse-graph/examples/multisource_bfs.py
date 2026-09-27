from collections import deque

def multisource_bfs(adj, sources):
    """BFS from multiple sources at once."""
    n = len(adj)
    dist = [-1] * n
    queue = deque()

    for src in sources:
        dist[src] = 0
        queue.append(src)

    while queue:
        u = queue.popleft()
        for v in adj[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                queue.append(v)

    return dist


adj = [
    [1, 2],
    [0, 3],
    [0, 4],
    [1, 5],
    [2, 5],
    [3, 4]
]

distances = multisource_bfs(adj, [0, 3])
print("Distances from sources [0, 3]:", distances)
