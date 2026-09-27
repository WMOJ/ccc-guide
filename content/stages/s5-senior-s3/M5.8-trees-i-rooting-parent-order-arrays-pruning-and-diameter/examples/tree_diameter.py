from collections import deque

def bfs_farthest(adj, start):
    """BFS from start, return (farthest_node, distance)."""
    n = len(adj)
    dist = [-1] * n
    dist[start] = 0
    queue = deque([start])
    farthest = start
    max_dist = 0

    while queue:
        u = queue.popleft()
        for v in adj[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                queue.append(v)
                if dist[v] > max_dist:
                    max_dist = dist[v]
                    farthest = v

    return farthest, max_dist


def tree_diameter(adj):
    """Find tree diameter using two BFS passes."""
    end1, _ = bfs_farthest(adj, 0)
    end2, diameter = bfs_farthest(adj, end1)
    return end1, end2, diameter


adj = [
    [1, 2],
    [0, 3],
    [0, 4, 5],
    [1],
    [2],
    [2]
]

end1, end2, diam = tree_diameter(adj)
print(f"Diameter endpoints: {end1}, {end2}")
print(f"Diameter: {diam}")
