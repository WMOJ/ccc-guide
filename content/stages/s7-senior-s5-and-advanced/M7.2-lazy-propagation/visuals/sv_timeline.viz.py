import vizrec as vz

rec = vz.Recorder()
n = int(rec.readline())
values = [int(x) for x in rec.readline().split()]
q = int(rec.readline())
ops = [list(map(int, rec.readline().split())) for _ in range(q)]

size = 1
while size < n:
    size *= 2
tree = [0] * (2 * size)
lazy = [0] * (2 * size)
for i in range(n):
    tree[size + i] = values[i]
for i in range(size - 1, 0, -1):
    tree[i] = tree[2 * i] + tree[2 * i + 1]

states = {}


def real(i):
    k = i
    while k < size:
        k *= 2
    return k - size < n


def build(i):
    kids = None
    if i < size:
        kids = [build(c) for c in (2 * i, 2 * i + 1) if real(c)]
    note = f"#{i}"
    if i < size and lazy[i] != 0:
        note += f" +{lazy[i]}"
    return vz.node(i, tree[i], children=kids, state=states.get(i), note=note)


covered = []
recomputed = []
pushed = []
received = []
stacked = []


def push(node, length):
    tag = lazy[node]
    if tag == 0:
        return
    pushed.append(node)
    half = length // 2
    tree[2 * node] += tag * half
    lazy[2 * node] += tag
    tree[2 * node + 1] += tag * half
    lazy[2 * node + 1] += tag
    lazy[node] = 0
    received.extend([2 * node, 2 * node + 1])


def update(node, node_lo, node_hi, l, r, v):
    if r <= node_lo or node_hi <= l:
        return
    if l <= node_lo and node_hi <= r:
        if node < size and lazy[node] != 0:
            stacked.append((node, lazy[node], lazy[node] + v))
        tree[node] += v * (node_hi - node_lo)
        lazy[node] += v
        covered.append(node)
        return
    push(node, node_hi - node_lo)
    mid = (node_lo + node_hi) // 2
    update(2 * node, node_lo, mid, l, r, v)
    update(2 * node + 1, mid, node_hi, l, r, v)
    tree[node] = tree[2 * node] + tree[2 * node + 1]
    recomputed.append(node)


def query(node, node_lo, node_hi, l, r):
    if r <= node_lo or node_hi <= l:
        return 0
    if l <= node_lo and node_hi <= r:
        covered.append(node)
        return tree[node]
    push(node, node_hi - node_lo)
    mid = (node_lo + node_hi) // 2
    return query(2 * node, node_lo, mid, l, r) + query(2 * node + 1, mid, node_hi, l, r)


def names(nodes, noun="node"):
    text = ", ".join(str(x) for x in nodes)
    return f"{noun} {text}" if len(nodes) == 1 else f"{noun}s {text}"


def frame(mark):
    states.clear()
    states.update(mark)
    return vz.tree(build(1))


rec.step(
    f"The {n} values sit in the leaves of a tree padded to {size} leaves. Each node shows its "
    "sum, and `#i` is its index. No tag is pending anywhere yet.",
    t=frame({})
)
answers = []
for number, op in enumerate(ops, start=1):
    covered.clear()
    recomputed.clear()
    pushed.clear()
    received.clear()
    stacked.clear()
    if op[0] == 1:
        _, l, r, v = op
        update(1, 0, size, l, r, v)
        inner = [c for c in covered if c < size]
        leaves = [c for c in covered if c >= size]
        parts = []
        if inner:
            parts.append(f"a tag on {names(inner)}")
        if leaves:
            parts.append(f"a direct change to {names(leaves, 'leaf')}".replace("leafs", "leaves"))
        mark = {c: "current" for c in covered}
        for x in recomputed:
            mark[x] = "done"
        for x in pushed:
            mark[x] = "compare"
        for x in received:
            mark[x] = "path"
        text = f"Operation {number}: add {v} to positions {l} up to, but not including, {r}. "
        text += "It wrote " + " and ".join(parts) + f"; the sums above were recomputed, so the root is now {tree[1]}."
        for node, old, new in stacked:
            text += f" Node {node} already held +{old}, so the two tags add up to +{new}."
        if pushed:
            text += f" Tags pushed down from {names(pushed)} on the way."
        rec.step(text, t=frame(mark))
    else:
        _, l, r = op
        answer = query(1, 0, size, l, r)
        answers.append(answer)
        mark = {c: "current" for c in covered}
        for x in pushed:
            mark[x] = "compare"
        for x in received:
            mark[x] = "path"
        text = (
            f"Operation {number}: sum positions {l} up to, but not including, {r}. It read "
            f"{names(covered)} and got {answer}."
        )
        if pushed:
            text += f" It pushed tags down from {names(pushed)} first."
        else:
            text += " No tag sat on its path, so nothing was pushed."
        rec.step(text, t=frame(mark))

rec.output("\n".join(str(a) for a in answers) + "\n")
