from collections import deque

import vizrec as vz

rec = vz.Recorder()
n = int(rec.readline())
adj = [[] for _ in range(n)]
for _ in range(n - 1):
    u, v = map(int, rec.readline().split())
    adj[u].append(v)
    adj[v].append(u)

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

LOG = max(1, max(depth).bit_length())
up = [parent]
for k in range(1, LOG):
    prev = up[k - 1]
    up.append([prev[x] for x in prev])

filled = [[k == 0 for k in range(LOG)] for _ in range(n)]
heads = [f"up[{k}]" for k in range(LOG)]


def pid(v):
    chain = [str(v)]
    while v != 0:
        v = parent[v]
        chain.append(str(v))
    return "-".join(reversed(chain))


def build(v, marks):
    return vz.node(pid(v), v, children=[build(c, marks) for c in kids[v]], state=marks.get(v), note=f"d{depth[v]}")


def frame(marks=None, compare=(), current=None):
    cells = [[up[k][v] if filled[v][k] else "-" for k in range(LOG)] for v in range(n)]
    states = {}
    for v in range(n):
        for k in range(LOG):
            if filled[v][k]:
                states[(v, k)] = "done"
    for cell in compare:
        states[cell] = "compare"
    if current is not None:
        states[current] = "current"
    return {
        "tree": vz.tree(build(0, marks or {})),
        "table": vz.table(cells, states=states, row_heads=list(range(n)), col_heads=heads, row_title="v"),
    }


rec.step(
    "Level 0 is the parent of every node, from the BFS. Node 0 is the root, so its parent is itself: "
    "a jump past the root stays on the root. The other columns are still empty (-).",
    **frame(),
)
for k in range(1, LOG):
    for v in range(n):
        mid = up[k - 1][v]
        res = up[k][v]
        filled[v][k] = True
        marks = {v: "current", mid: "compare"}
        if res not in marks:
            marks[res] = "path"
        if mid == v:
            how = f"Node {v} is the root, so both halves stay on {v}."
        else:
            how = f"From node {v}, {1 << (k - 1)} {'step' if k == 1 else 'steps'} up reach node {mid}, and {1 << (k - 1)} more reach node {res}."
        rec.step(
            f"up[{k}][{v}] = up[{k - 1}][up[{k - 1}][{v}]] = up[{k - 1}][{mid}] = {res}. {how}",
            **frame(marks, compare=[(v, k - 1), (mid, k - 1)], current=(v, k)),
        )
last = LOG - 1
rec.step(
    f"The table is full. Level {last} holds the node {1 << last} steps up, or the root if the walk would pass it.",
    **frame(),
)
out = [f"depth = {depth}"] + [f"up[{k}] = {up[k]}" for k in range(LOG)]
rec.output("\n".join(out) + "\n")
