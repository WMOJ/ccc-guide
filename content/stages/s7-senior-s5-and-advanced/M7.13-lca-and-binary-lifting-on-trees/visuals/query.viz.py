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

LOG = max(1, max(depth).bit_length())
up = [parent]
for k in range(1, LOG):
    prev = up[k - 1]
    up.append([prev[z] for z in prev])

x, y = a0, b0
head = "up[0]"
test = ["-", "-"]
targets = {}


def pid(v):
    chain = [str(v)]
    while v != 0:
        v = parent[v]
        chain.append(str(v))
    return "-".join(reversed(chain))


def build(v):
    if v == x and v == y:
        state = "path"
    elif v == x:
        state = "current"
    elif v == y:
        state = "compare"
    else:
        state = targets.get(v)
    return vz.node(pid(v), v, children=[build(c) for c in kids[v]], state=state, note=f"d{depth[v]}")


def frame(tstates=None):
    cells = [[x, y], [depth[x], depth[y]], test]
    return {
        "tree": vz.tree(build(0)),
        "table": vz.table(cells, states=tstates, row_heads=["node", "depth", head], col_heads=["a", "b"]),
    }


rec.step(
    f"Find the lowest common ancestor of {a0} and {b0}. Node {a0} is at depth {depth[a0]} and node {b0} at "
    f"depth {depth[b0]}. The table keeps the two nodes, their depths and the level being tried.",
    **frame(),
)
if depth[x] < depth[y]:
    x, y = y, x
    rec.step(
        f"Node {y} is shallower, so swap the names: a = {x} is now the deeper node, at depth {depth[x]}.",
        **frame(),
    )
diff = depth[x] - depth[y]
if diff == 0:
    rec.step("The depths are equal, so there is nothing to equalize.", **frame())
else:
    bits = [k for k in range(LOG) if (diff >> k) & 1]
    rec.step(
        f"The depth difference is {diff}, which is {format(diff, 'b')} in binary. a must climb "
        f"{diff} {'level' if diff == 1 else 'levels'}"
        + (f", as {' + '.join(str(1 << k) for k in bits)}" if len(bits) > 1 else "")
        + ", with one table lookup per set bit, lowest bit first.",
        **frame(),
    )
    for k in bits:
        old = x
        x = up[k][x]
        head = f"up[{k}]"
        test = [x, "-"]
        rec.step(
            f"Bit {k} of {diff} is set: a = up[{k}][{old}] = {x}, a climb of {1 << k} "
            f"{'level' if k == 0 else 'levels'}. a is now at depth {depth[x]}.",
            **frame(["__", "__", "c_"]),
        )
        test = ["-", "-"]
        head = "up[0]"
if x == y:
    rec.step(
        f"a and b are now the same node, {x}: b was an ancestor of a. No jump together is needed, and the "
        f"answer is {x}.",
        **frame(),
    )
else:
    rec.step(
        f"Both nodes are at depth {depth[x]} and they differ. Now try the levels from the highest, "
        f"k = {LOG - 1}, down to 0, and jump both only when their targets differ.",
        **frame(),
    )
    for k in reversed(range(LOG)):
        ta, tb = up[k][x], up[k][y]
        head = f"up[{k}]"
        test = [ta, tb]
        if ta != tb:
            targets = {ta: "frontier", tb: "frontier"}
            rec.step(
                f"Level {k}: up[{k}][{x}] = {ta} and up[{k}][{y}] = {tb} differ, so both are still below "
                f"the answer. Jump: a = {ta}, b = {tb}.",
                **frame(["__", "__", "mm"]),
            )
            x, y = ta, tb
            targets = {}
            test = ["-", "-"]
            rec.step(
                f"a and b now sit at node {x} and node {y}, at depth {depth[x]}.",
                **frame(),
            )
        else:
            targets = {ta: "invalid"}
            rec.step(
                f"Level {k}: up[{k}][{x}] and up[{k}][{y}] are both {ta}. That is the common ancestor or "
                f"above it, so jumping could overshoot. Skip this level.",
                **frame(["__", "__", "xx"]),
            )
            targets = {}
            test = ["-", "-"]
    answer = up[0][x]
    targets = {answer: "path"}
    head = "up[0]"
    test = [answer, answer]
    rec.step(
        f"Every level is tried. a = {x} and b = {y} are different nodes with the same parent, so the "
        f"answer is up[0][{x}] = {answer}.",
        **frame(["__", "__", "mm"]),
    )
    targets = {}
    x = y = answer
    test = ["-", "-"]
dist = depth[a0] + depth[b0] - 2 * depth[x]
rec.step(
    f"The lowest common ancestor of {a0} and {b0} is node {x}, at depth {depth[x]}. The path between "
    f"them has {depth[a0]} + {depth[b0]} - 2 * {depth[x]} = {dist} edges.",
    **frame(),
)
rec.output(f"{x} {dist}\n")
