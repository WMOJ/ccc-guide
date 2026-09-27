def iterative_postorder_dfs(adj, root):
    """Iterative postorder DFS using a marker technique."""
    visited = set()
    stack = [root]
    order = []
    MARKER = None

    while stack:
        node = stack[-1]
        if node is MARKER or node in visited:
            stack.pop()
            if node is not MARKER:
                order.append(node)
            continue

        visited.add(node)
        stack.append(MARKER)
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

result = iterative_postorder_dfs(adj, 0)
print("Postorder DFS:", result)
