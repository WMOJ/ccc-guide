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
a0, b0 = map(int, rec.readline().split())

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

a, b = a0, b0
seen = {a, b}
moves = 0


def pid(v):
    chain = [str(v)]
    while v != 0:
        v = parent[v]
        chain.append(str(v))
    return "-".join(reversed(chain))


def build(v):
    if a == b and v == a:
        state = "path"
    elif v == a:
        state = "current"
    elif v == b:
        state = "compare"
    elif v in seen:
        state = "done"
    else:
        state = None
    return vz.node(pid(v), v, children=[build(c) for c in kids[v]], state=state, note=f"d{depth[v]}")


def frame():
    tree = vz.tree(build(0))
    table = vz.table([[a, depth[a]], [b, depth[b]], [moves, "-"]], row_heads=["a", "b", "moves"],
                     col_heads=["node", "depth"])
    return {"tree": tree, "table": table}


rec.step(
    f"Find the lowest common ancestor of a = {a0} and b = {b0}. Each node shows its depth, such as d{depth[a0]}. "
    f"Node {a0} is at depth {depth[a0]} and node {b0} at depth {depth[b0]}. No parent moves yet.",
    **frame(),
)
while depth[a] > depth[b]:
    old = a
    a = parent[a]
    moves += 1
    seen.add(a)
    rec.step(
        f"a is deeper than b ({depth[old]} against {depth[b]}), so a moves up to its parent: "
        f"node {old} to node {a}. That is parent move {moves}.",
        **frame(),
    )
while depth[b] > depth[a]:
    old = b
    b = parent[b]
    moves += 1
    seen.add(b)
    rec.step(
        f"b is deeper than a ({depth[old]} against {depth[a]}), so b moves up to its parent: "
        f"node {old} to node {b}. That is parent move {moves}.",
        **frame(),
    )
if a != b:
    rec.step(
        f"Both nodes are at depth {depth[a]}, but {a} and {b} are different nodes. Move both up together "
        f"until they meet.",
        **frame(),
    )
    while a != b:
        oa, ob = a, b
        a = parent[a]
        b = parent[b]
        moves += 2
        seen.add(a)
        seen.add(b)
        if a == b:
            text = f"Both move up: {oa} to {a} and {ob} to {b}. They are the same node, so {a} is the answer."
        else:
            text = f"Both move up: {oa} to {a} and {ob} to {b}. Still different nodes."
        rec.step(text + f" Parent moves so far: {moves}.", **frame())
rec.step(
    f"The lowest common ancestor of {a0} and {b0} is node {a}. This query cost {moves} parent "
    f"{'move' if moves == 1 else 'moves'}, and every query pays its own walk.",
    **frame(),
)
rec.output(f"{a}\nparent moves: {moves}\n")
