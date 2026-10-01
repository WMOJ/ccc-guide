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


def stack_view(stack):
    return [(f"{v}{'*' if ready else ''}", None) for v, ready in stack]


def frame(node_states, stack):
    return {
        "tree": vz.tree(build_node(0, node_states)),
        "stack": vz.stack(stack_view(stack), name="stack"),
    }


seen = [False] * n
stack = [(0, False)]
order = []
node_states = {}
rec.step(
    "The stack starts with the root, entered but not yet ready to record. A marked entry "
    'with a "*" means: record this vertex once every child pushed under it is done.',
    **frame(node_states, stack)
)

while stack:
    node, ready = stack.pop()
    if ready:
        order.append(node)
        node_states = dict(node_states)
        node_states[node] = "done"
        rec.step(
            f"Vertex {node}'s marker comes off the stack. Every child under it has already "
            f"been recorded, so vertex {node} is recorded now, at postorder position "
            f"{len(order) - 1}.",
            **frame(node_states, stack)
        )
        continue
    if seen[node]:
        continue
    seen[node] = True
    node_states = dict(node_states)
    node_states[node] = "current"
    stack.append((node, True))
    pushed = []
    for neighbor in reversed(adj[node]):
        if not seen[neighbor]:
            stack.append((neighbor, False))
            pushed.append(neighbor)
    if pushed:
        names = ", ".join(str(v) for v in pushed)
        what = (
            f"its unvisited child{'ren' if len(pushed) > 1 else ''} {names} enter"
            f"{'s' if len(pushed) == 1 else ''} the stack above it, so they will be recorded "
            "first."
        )
    else:
        what = "it has no children, so its own marker is next on the stack."
    rec.step(
        f"Vertex {node} enters the stack: {what}",
        **frame(node_states, stack)
    )

rec.step(
    f"The stack is empty. Every vertex has been recorded once its children were, giving the "
    f"postorder {order}.",
    **frame(node_states, [])
)

lines = [f"Postorder: {order}"]
rec.output("\n".join(lines) + "\n")
