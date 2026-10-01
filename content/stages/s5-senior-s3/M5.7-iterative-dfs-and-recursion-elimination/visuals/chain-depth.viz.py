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

seen = [False] * n
stack = [0]
order = []
deepest = 0

rec.step(
    "The stack starts with just the root. This chain is 8 vertices long, far too deep for a "
    "small recursion limit, but the stack holds one entry.",
    stack=vz.stack([(str(0), None)], name="stack")
)

while stack:
    node = stack.pop()
    if seen[node]:
        continue
    seen[node] = True
    order.append(node)
    deepest = max(deepest, len(order))
    for neighbor in reversed(adj[node]):
        if not seen[neighbor]:
            stack.append(neighbor)
    rec.step(
        f"Vertex {node} is visited: visit number {len(order)} of {n}. A recursive DFS would "
        f"now be {len(order)} calls deep on its own call stack; this explicit stack still "
        "holds at most one waiting vertex.",
        stack=vz.stack([(str(v), None) for v in stack], name="stack")
    )

rec.step(
    f"Every vertex is visited. A recursive version needed a call stack {deepest} frames deep to "
    "reach the far end; this loop never held more than one entry on its own stack.",
    stack=vz.stack([], name="stack")
)

lines = [f"Preorder: {order}"]
rec.output("\n".join(lines) + "\n")
