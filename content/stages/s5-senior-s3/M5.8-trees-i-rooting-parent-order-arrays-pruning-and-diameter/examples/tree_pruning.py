from collections import deque

def prune_leaves(adj):
    """Prune leaves layer by layer."""
    n = len(adj)
    degree = [len(adj[i]) for i in range(n)]
    queue = deque([i for i in range(n) if degree[i] <= 1])
    layers = []

    while queue:
        layer = []
        for _ in range(len(queue)):
            u = queue.popleft()
            layer.append(u)
            for v in adj[u]:
                degree[v] -= 1
                if degree[v] == 1:
                    queue.append(v)
        layers.append(layer)

    return layers


adj = [
    [1, 2],
    [0, 3, 4],
    [0, 5],
    [1],
    [1],
    [2]
]

layers = prune_leaves(adj)
for i, layer in enumerate(layers):
    print(f"Layer {i}: {layer}")
