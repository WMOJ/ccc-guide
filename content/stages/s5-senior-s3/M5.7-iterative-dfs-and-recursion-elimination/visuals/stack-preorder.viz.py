import vizrec as vz

rec = vz.Recorder()
n, m = map(int, rec.readline().split())
edges = []
for _ in range(m):
    a, b = map(int, rec.readline().split())
    edges.append((a, b))

adj = [[] for _ in range(n)]
for a, b in edges:
    adj[a].append(b)
    adj[b].append(a)


def build_children(root):
    parent = [None] * n
    children = [[] for _ in range(n)]
    seen = [False] * n
    seen[root] = True
    todo = [root]
    while todo:
        u = todo.pop()
        for v in adj[u]:
            if not seen[v]:
                seen[v] = True
                parent[v] = u
                children[u].append(v)
                todo.append(v)
    return children


children = build_children(0)


def build_node(u, node_states):
    kids = [build_node(c, node_states) for c in children[u]]
    return vz.node(f"n{n}_{u}", str(u), children=kids, state=node_states.get(u, "unvisited"))


def frame(node_states, stack_view):
    return {
        "tree": vz.tree(build_node(0, node_states)),
        "stack": vz.stack(stack_view, name="stack"),
    }


seen = [False] * n
stack = [0]
order = []
node_states = {}
rec.step(
    "The stack starts with just the root, vertex 0. Every other vertex is still unvisited.",
    **frame(node_states, [(str(0), None)])
)

while stack:
    node = stack.pop()
    if seen[node]:
        node_states = dict(node_states)
        rec.step(
            f"Vertex {node} comes off the stack again, but it is already visited, so this pop "
            "is skipped and nothing changes.",
            **frame(node_states, [(str(v), None) for v in stack])
        )
        continue
    seen[node] = True
    order.append(node)
    node_states = dict(node_states)
    node_states[node] = "current"
    pushed = []
    for neighbor in reversed(adj[node]):
        if not seen[neighbor]:
            stack.append(neighbor)
            pushed.append(neighbor)
    stack_view = [(str(v), None) for v in stack]
    if pushed:
        names = ", ".join(str(v) for v in pushed)
        what = f"its unvisited neighbor{'s' if len(pushed) > 1 else ''} {names} join{'s' if len(pushed) == 1 else ''} the stack."
    else:
        what = "it has no unvisited neighbors, so nothing joins the stack."
    rec.step(
        f"Vertex {node} is popped and marked visited, order position {len(order) - 1}: {what}",
        **frame(node_states, stack_view)
    )
    node_states[node] = "done"

rec.step(
    f"The stack is empty. Every vertex has been visited once, in the order {order}.",
    **frame(node_states, [])
)

lines = [f"Preorder: {order}"]
rec.output("\n".join(lines) + "\n")
