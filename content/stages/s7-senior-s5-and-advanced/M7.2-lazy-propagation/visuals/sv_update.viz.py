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

recording = False
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


def step(caption):
    if recording:
        rec.step(caption, t=vz.tree(build(1)))


def push(node, length):
    """Push node's tag to its children. Returns the sentence describing what happened."""
    tag = lazy[node]
    if tag == 0:
        return "It holds no tag to push down."
    half = length // 2
    tree[2 * node] += tag * half
    lazy[2 * node] += tag
    tree[2 * node + 1] += tag * half
    lazy[2 * node + 1] += tag
    lazy[node] = 0
    states[2 * node] = "path"
    states[2 * node + 1] = "path"
    return (
        f"It holds tag +{tag}, so push that down first: each child gets {tag} x {half} = "
        f"{tag * half} added to its sum and +{tag} added to its tag, and node {node}'s tag "
        "is cleared."
    )


def update(node, node_lo, node_hi, l, r, v):
    if r <= node_lo or node_hi <= l:
        states[node] = "invalid"
        step(f"Node {node} covers [{node_lo}, {node_hi}), outside [{l}, {r}). Return at once.")
        return
    if l <= node_lo and node_hi <= r:
        length = node_hi - node_lo
        tree[node] += v * length
        lazy[node] += v
        states[node] = "current"
        if node >= size:
            tail = "It is a leaf, so there is nothing below it."
        else:
            tail = (
                f"+{v} joins its tag for its {length} leaves, and none of them is visited."
            )
        step(
            f"Node {node} covers [{node_lo}, {node_hi}), inside [{l}, {r}). Its sum gains "
            f"{v} x {length} = {v * length}. {tail}"
        )
        return
    states[node] = "compare"
    pushed = push(node, node_hi - node_lo)
    step(
        f"Node {node} covers [{node_lo}, {node_hi}), partly inside [{l}, {r}), so both "
        f"children must be visited. {pushed}"
    )
    mid = (node_lo + node_hi) // 2
    update(2 * node, node_lo, mid, l, r, v)
    update(2 * node + 1, mid, node_hi, l, r, v)
    tree[node] = tree[2 * node] + tree[2 * node + 1]
    states[node] = "done"
    step(
        f"Both children of node {node} are finished, so `tree[{node}] = tree[{2 * node}] + "
        f"tree[{2 * node + 1}]` = {tree[2 * node]} + {tree[2 * node + 1]} = {tree[node]}."
    )


def query(node, node_lo, node_hi, l, r):
    if r <= node_lo or node_hi <= l:
        return 0
    if l <= node_lo and node_hi <= r:
        return tree[node]
    push(node, node_hi - node_lo)
    mid = (node_lo + node_hi) // 2
    return query(2 * node, node_lo, mid, l, r) + query(2 * node + 1, mid, node_hi, l, r)


last_update = max(i for i, op in enumerate(ops) if op[0] == 1)
answers = []
for idx, op in enumerate(ops):
    if op[0] == 1:
        _, l, r, v = op
        if idx == last_update:
            recording = True
            owed = [i for i in range(1, size) if lazy[i] != 0]
            pending = ""
            if owed:
                pending = (
                    f" Node{'s' if len(owed) != 1 else ''} "
                    f"{', '.join(str(i) for i in owed)} already hold"
                    f"{'' if len(owed) != 1 else 's'} a tag from an earlier update."
                )
            step(
                f"Add {v} to positions {l} up to, but not including, {r}. Each node shows "
                "its sum, and a tag (+n) beside it is an update still owed to its children."
                + pending
            )
            update(1, 0, size, l, r, v)
            covered = [i for i in range(1, 2 * size) if states.get(i) == "current"]
            inner = [str(i) for i in covered if i < size]
            leaves = [str(i) for i in covered if i >= size]
            states.clear()
            parts = []
            if inner:
                if len(inner) == 1:
                    parts.append(f"a tag on node {inner[0]}")
                else:
                    parts.append(f"tags on nodes {', '.join(inner)}")
            if leaves:
                if len(leaves) == 1:
                    parts.append(f"a direct change to leaf {leaves[0]}")
                else:
                    parts.append(f"direct changes to leaves {', '.join(leaves)}")
            step(
                f"Done. This update wrote {' and '.join(parts)}. Everything beneath a tag "
                "still holds old values, and a later visit will push the tag down."
            )
            recording = False
        else:
            update(1, 0, size, l, r, v)
    else:
        answers.append(query(1, 0, size, op[1], op[2]))

rec.output("\n".join(str(a) for a in answers) + "\n")
