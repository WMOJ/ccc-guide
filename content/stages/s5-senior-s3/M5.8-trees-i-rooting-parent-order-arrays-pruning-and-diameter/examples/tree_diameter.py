import sys
from collections import deque


def build_adjacency(n: int, edges: list) -> list:
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    return adj


def bfs_farthest(adj: list, start: int) -> tuple:
    """BFS from start; return the farthest node found and its distance."""
    n = len(adj)
    dist = [-1] * n
    dist[start] = 0
    queue = deque([start])
    farthest = start
    max_dist = 0
    while queue:
        node = queue.popleft()
        for neighbor in adj[node]:
            if dist[neighbor] == -1:
                dist[neighbor] = dist[node] + 1
                queue.append(neighbor)
                if dist[neighbor] > max_dist:
                    max_dist = dist[neighbor]
                    farthest = neighbor
    return farthest, max_dist


def tree_diameter(adj: list) -> tuple:
    """Diameter by two BFS passes: any start to one end, then that end to the other."""
    end_a, _ = bfs_farthest(adj, 0)
    end_b, length = bfs_farthest(adj, end_a)
    return end_a, end_b, length


def main() -> None:
    data = sys.stdin.read().split()
    if not data:
        return

    pos = 0
    n = int(data[pos])
    pos += 1

    edges = []
    for _ in range(n - 1):
        a = int(data[pos])
        b = int(data[pos + 1])
        pos += 2
        edges.append((a, b))

    adj = build_adjacency(n, edges)
    end_a, end_b, length = tree_diameter(adj)
    print("Diameter endpoints:", end_a, end_b)
    print("Diameter:", length)


if __name__ == "__main__":
    main()
