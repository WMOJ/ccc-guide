import sys
from collections import deque


def build_adjacency(n: int, edges: list) -> list:
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    return adj


def prune_unimportant_leaves(n: int, adj: list, important: list) -> tuple:
    """Repeatedly remove leaves that are not important, layer by layer."""
    degree = [len(adj[i]) for i in range(n)]
    removed = [False] * n
    queue = deque(i for i in range(n) if degree[i] == 1 and not important[i])
    removed_edges = 0
    while queue:
        node = queue.popleft()
        if removed[node]:
            continue
        removed[node] = True
        for neighbor in adj[node]:
            if removed[neighbor]:
                continue
            degree[neighbor] -= 1
            removed_edges += 1
            if degree[neighbor] == 1 and not important[neighbor]:
                queue.append(neighbor)
    kept = [i for i in range(n) if not removed[i]]
    return kept, removed_edges


def main() -> None:
    data = sys.stdin.read().split()
    if not data:
        return

    pos = 0
    n = int(data[pos])
    k = int(data[pos + 1])
    pos += 2

    important = [False] * n
    for _ in range(k):
        important[int(data[pos])] = True
        pos += 1

    edges = []
    for _ in range(n - 1):
        a = int(data[pos])
        b = int(data[pos + 1])
        pos += 2
        edges.append((a, b))

    adj = build_adjacency(n, edges)
    kept, removed_edges = prune_unimportant_leaves(n, adj, important)
    print("Rooms kept:", kept)
    print("Hallways closed:", removed_edges)


if __name__ == "__main__":
    main()
