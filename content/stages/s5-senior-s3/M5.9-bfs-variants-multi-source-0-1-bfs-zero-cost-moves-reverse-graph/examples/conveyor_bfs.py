from collections import deque

def conveyor_bfs(adj, conveyors, start):
    """BFS handling forced zero-cost moves (conveyors)."""
    n = len(adj)
    dist = [-1] * n
    visited = [False] * n

    def follow_conveyors(u, in_progress):
        """Follow zero-cost moves, detect cycles."""
        if in_progress[u]:
            return u
        in_progress[u] = True
        if u in conveyors:
            u = follow_conveyors(conveyors[u], in_progress)
        in_progress[u] = False
        return u

    dist[start] = 0
    queue = deque([start])

    while queue:
        u = queue.popleft()
        u = follow_conveyors(u, [False] * n)
        if visited[u]:
            continue
        visited[u] = True

        for v in adj[u]:
            if not visited[v]:
                dist[v] = dist[u] + 1
                queue.append(v)

    return dist


adj = {
    0: [1, 2],
    1: [3],
    2: [4],
    3: [5],
    4: [5],
    5: []
}
conveyors = {1: 2}

distances = conveyor_bfs(adj, conveyors, 0)
print("Distances with conveyors:", distances)
