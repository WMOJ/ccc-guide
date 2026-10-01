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

dp0 = [0] * n
dp1 = [1] * n


def build(node, done, current, path=""):
    path = f"{path}-{node}"
    kids = [build(c, done, current, path) for c in range(n) if parent[c] == node]
    if node == current:
        state = "current"
    elif node in done:
        state = "done"
    else:
        state = None
    return vz.node(path, str(node), children=kids, state=state,
                   edge="done" if node in done else None,
                   note=f"{dp0[node]}/{dp1[node]}")


def frame(done, current=None):
    return {
        "t": vz.tree(build(0, done, current)),
        "arr": vz.table(
            [dp0, dp1],
            row_heads=["dp0", "dp1"],
            col_heads=list(range(n)),
            row_title="node",
        ),
    }


rec.step(
    f"The tree is rooted at node 0 and the BFS order is {order}. Every node starts with dp0 = 0 "
    "(nothing chosen below it yet) and dp1 = 1 (itself). Each node shows dp0/dp1.",
    **frame(set())
)
done = set()
for i in range(n - 1, 0, -1):
    u = order[i]
    p = parent[u]
    b0, b1 = dp0[p], dp1[p]
    add0 = max(dp0[u], dp1[u])
    add1 = dp0[u]
    dp0[p] += add0
    dp1[p] += add1
    done.add(u)
    rec.step(
        f"Node {u} is final: dp0 is {dp0[u]}, dp1 is {dp1[u]}. Folding it into parent {p}: "
        f"dp0[{p}] gains max({dp0[u]}, {dp1[u]}) = {add0}, from {b0} to {dp0[p]}; "
        f"dp1[{p}] gains dp0[{u}] = {add1}, from {b1} to {dp1[p]}.",
        **frame(done, current=p)
    )
best = max(dp0[0], dp1[0])
choice = "leaving node 0 out" if dp0[0] >= dp1[0] else "choosing node 0"
rec.step(
    f"Node 0 is the root, so nothing folds it upward. dp0[0] = {dp0[0]} and dp1[0] = {dp1[0]}; "
    f"the largest independent set has max({dp0[0]}, {dp1[0]}) = {best} nodes, found by {choice}.",
    **frame(done, current=0)
)
rec.output(
    f"Order: {order}\ndp0: {dp0}\ndp1: {dp1}\nLargest set: {best}\n"
)
