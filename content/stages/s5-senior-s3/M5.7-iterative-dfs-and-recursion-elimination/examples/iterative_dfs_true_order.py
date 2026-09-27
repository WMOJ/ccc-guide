def iterative_dfs_true_order(adj, root):
    """Iterative DFS with iterator indices for true DFS order."""
    visited = set()
    stack = [(root, 0)]
    order = []

    while stack:
        node, idx = stack[-1]
        if node in visited and idx == 0:
            stack.pop()
            continue
        if idx == 0:
            visited.add(node)
            order.append(node)

        if idx < len(adj[node]):
            neighbor = adj[node][idx]
            stack[-1] = (node, idx + 1)
            if neighbor not in visited:
                stack.append((neighbor, 0))
        else:
            stack.pop()

    return order


adj = {
    0: [1, 2],
    1: [3, 4],
    2: [5],
    3: [],
    4: [],
    5: []
}

result = iterative_dfs_true_order(adj, 0)
print("DFS with iterator order:", result)
