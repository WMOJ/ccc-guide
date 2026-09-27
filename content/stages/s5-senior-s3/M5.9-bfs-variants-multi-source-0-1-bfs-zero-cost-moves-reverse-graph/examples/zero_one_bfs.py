from collections import deque

def zero_one_bfs(adj, start):
    """0-1 BFS using deque with appendleft for weight-0 edges."""
    n = len(adj)
    dist = [float('inf')] * n
    dist[start] = 0
    queue = deque([start])

    while queue:
        u = queue.popleft()
        for v, w in adj[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                if w == 0:
                    queue.appendleft(v)
                else:
                    queue.append(v)

    return dist


adj = [
    [(1, 0), (2, 1)],
    [(0, 0), (3, 1)],
    [(0, 1), (4, 0)],
    [(1, 1), (5, 1)],
    [(2, 0), (5, 1)],
    [(3, 1), (4, 1)]
]

distances = zero_one_bfs(adj, 0)
print("0-1 BFS distances from node 0:", distances)
