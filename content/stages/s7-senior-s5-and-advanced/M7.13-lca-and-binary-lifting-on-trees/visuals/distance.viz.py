from collections import deque

import vizrec as vz

rec = vz.Recorder()
n = int(rec.readline())
adj = [[] for _ in range(n)]
for _ in range(n - 1):
    u, v = map(int, rec.readline().split())
    adj[u].append(v)
    adj[v].append(u)
rec.readline()
a, b = map(int, rec.readline().split())

parent = [0] * n
depth = [-1] * n
depth[0] = 0
queue = deque([0])
while queue:
    node = queue.popleft()
    for nb in adj[node]:
        if depth[nb] == -1:
            depth[nb] = depth[node] + 1
            parent[nb] = node
            queue.append(nb)
kids = [[] for _ in range(n)]
for v in range(1, n):
    kids[parent[v]].append(v)


def climb(v, stop):
    chain = []
    while v != stop:
        chain.append(v)
        v = parent[v]
    return chain


x, y = a, b
while depth[x] > depth[y]:
    x = parent[x]
while depth[y] > depth[x]:
    y = parent[y]
while x != y:
    x = parent[x]
    y = parent[y]
lca = x
left = climb(a, lca)
right = climb(b, lca)
dist = len(left) + len(right)


def pid(v):
    chain = [str(v)]
    while v != 0:
        v = parent[v]
        chain.append(str(v))
    return "-".join(reversed(chain))


def build(v, on_a, on_b, marks):
    if v == lca and "lca" in marks:
        state = "current"
    elif v in on_a:
        state = "path"
    elif v in on_b:
        state = "compare"
    elif v in (a, b):
        state = "frontier"
    else:
        state = None
    edge = "path" if (v in on_a or v in on_b) else None
    return vz.node(pid(v), v, children=[build(c, on_a, on_b, marks) for c in kids[v]], state=state,
                   note=f"d{depth[v]}", edge=edge)


def frame(on_a=(), on_b=(), marks=()):
    return {"tree": vz.tree(build(0, set(on_a), set(on_b), marks))}


rec.step(
    f"Two nodes: {a} at depth {depth[a]} and {b} at depth {depth[b]}. The distance between them is the "
    f"number of edges on the one path that joins them.",
    **frame(),
)
rec.step(
    f"The lowest common ancestor is node {lca}, at depth {depth[lca]}. The path from {a} to {b} must pass "
    f"through it.",
    **frame(marks=("lca",)),
)
if left:
    rec.step(
        f"From {a} up to {lca} is {depth[a]} - {depth[lca]} = {len(left)} "
        f"{'edge' if len(left) == 1 else 'edges'}, marked on the tree.",
        **frame(left, marks=("lca",)),
    )
else:
    rec.step(f"Node {a} is the lowest common ancestor itself, so this side has 0 edges.", **frame(marks=("lca",)))
if right:
    rec.step(
        f"From {lca} down to {b} is {depth[b]} - {depth[lca]} = {len(right)} "
        f"{'edge' if len(right) == 1 else 'edges'}.",
        **frame(left, right, marks=("lca",)),
    )
else:
    rec.step(f"Node {b} is the lowest common ancestor itself, so this side has 0 edges.", **frame(left, marks=("lca",)))
rec.step(
    f"Together: depth[{a}] + depth[{b}] - 2 * depth[{lca}] = {depth[a]} + {depth[b]} - {2 * depth[lca]} "
    f"= {dist} edges. Both depths include the {depth[lca]} edges from the root to {lca}, which are not on the path, so subtract them twice.",
    **frame(left, right, marks=("lca",)),
)
rec.output(f"{lca} {dist}\n")
