def iterative_dfs(adj, root):
    """Iterative DFS starting from root."""
    visited = set()
    stack = [root]
    order = []

    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        order.append(node)

        for neighbor in reversed(adj[node]):
            if neighbor not in visited:
                stack.append(neighbor)

    return order


adj = {
    0: [1, 2],
    1: [3, 4],
    2: [5],
    3: [],
    4: [],
    5: []
}

result = iterative_dfs(adj, 0)
print("DFS order:", result)
