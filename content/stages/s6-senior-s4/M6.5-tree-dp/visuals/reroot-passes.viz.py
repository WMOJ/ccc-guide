from collections import deque

import vizrec as vz

rec = vz.Recorder()
n = int(rec.readline())
adj = [[] for _ in range(n)]
for _ in range(n - 1):
    a, b = map(int, rec.readline().split())
    adj[a].append(b)
    adj[b].append(a)

parent = [-1] * n
seen = [False] * n
order = []
seen[0] = True
queue = deque([0])
while queue:
    u = queue.popleft()
    order.append(u)
    for v in adj[u]:
        if not seen[v]:
            seen[v] = True
            parent[v] = u
            queue.append(v)

size = [1] * n
down = [0] * n
ans = [None] * n
phase = 1


def build(node, done, current, path=""):
    path = f"{path}-{node}"
    kids = [build(c, done, current, path) for c in range(n) if parent[c] == node]
    if node == current:
        state = "current"
    elif node in done:
        state = "done"
    else:
        state = None
    if phase == 1:
        note = f"{size[node]}|{down[node]}"
    else:
        note = f"a={ans[node]}" if ans[node] is not None else None
    return vz.node(path, str(node), children=kids, state=state,
                   edge="done" if node in done else None, note=note)


def frame(done, current=None):
    return {
        "t": vz.tree(build(0, done, current)),
        "arr": vz.table(
            [size, down, ans],
            row_heads=["size", "down", "ans"],
            col_heads=list(range(n)),
            row_title="node",
        ),
    }


rec.step(
    f"Pass 1 walks the BFS order {order} backward. Each node starts with size 1 (itself) and "
    "down 0 (the distances to its own descendants, none yet). Each node shows size|down.",
    **frame(set())
)
done = set()
for i in range(n - 1, 0, -1):
    u = order[i]
    p = parent[u]
    s = size[u]
    size[p] += s
    down[p] += down[u] + s
    done.add(u)
    rec.step(
        f"Node {u} has size {s} and down {down[u]}. Folding it into parent {p}: every node of "
        f"{u}'s subtree ({s} in all) is one edge farther from {p} than from {u}, so down[{p}] "
        f"grows by down[{u}] + {s} and is now {down[p]}; size[{p}] is now {size[p]}.",
        **frame(done, current=p)
    )
phase = 2
ans[0] = down[0]
done = {0}
rec.step(
    f"Pass 2 starts at the root. With the tree rooted at 0, down[0] = {down[0]} is already the "
    f"sum of distances from 0 to every node, so ans[0] = {ans[0]}. The tree now shows ans.",
    **frame(done, current=0)
)
for i in range(1, n):
    u = order[i]
    p = parent[u]
    s = size[u]
    far = n - s
    ans[u] = ans[p] - s + far
    done.add(u)
    rec.step(
        f"Moving the root from {p} to {u}: the {s} {'node' if s == 1 else 'nodes'} in {u}'s subtree "
        f"{'gets' if s == 1 else 'get'} one edge closer ({s} fewer). The other {far} "
        f"{'node' if far == 1 else 'nodes'} {'gets' if far == 1 else 'get'} one edge farther "
        f"({far} more). ans[{u}] = {ans[p]} - {s} + {far} = {ans[u]}.",
        **frame(done, current=u)
    )
rec.output(f"Size: {size}\nDown: {down}\nAnswer: {ans}\n")
