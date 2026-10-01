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
pushes = []


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
    pushes.append(node)
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
        "is cleared. Now both children can be trusted."
    )


def update(node, node_lo, node_hi, l, r, v):
    if r <= node_lo or node_hi <= l:
        return
    if l <= node_lo and node_hi <= r:
        tree[node] += v * (node_hi - node_lo)
        lazy[node] += v
        return
    push(node, node_hi - node_lo)
    mid = (node_lo + node_hi) // 2
    update(2 * node, node_lo, mid, l, r, v)
    update(2 * node + 1, mid, node_hi, l, r, v)
    tree[node] = tree[2 * node] + tree[2 * node + 1]


reads = []


def query(node, node_lo, node_hi, l, r):
    if r <= node_lo or node_hi <= l:
        states[node] = "invalid"
        step(f"Node {node} covers [{node_lo}, {node_hi}), outside [{l}, {r}). It adds 0.")
        return 0
    if l <= node_lo and node_hi <= r:
        states[node] = "current"
        reads.append(tree[node])
        step(
            f"Node {node} covers [{node_lo}, {node_hi}), inside [{l}, {r}). Its sum, "
            f"`tree[{node}]` = {tree[node]}, is exactly right, so it is returned without "
            "looking below."
        )
        return tree[node]
    states[node] = "compare"
    pushed = push(node, node_hi - node_lo)
    step(
        f"Node {node} covers [{node_lo}, {node_hi}), partly inside [{l}, {r}). {pushed}"
    )
    mid = (node_lo + node_hi) // 2
    return query(2 * node, node_lo, mid, l, r) + query(2 * node + 1, mid, node_hi, l, r)


last_query = max(i for i, op in enumerate(ops) if op[0] == 2)
answers = []
for idx, op in enumerate(ops):
    if op[0] == 1:
        _, l, r, v = op
        update(1, 0, size, l, r, v)
    elif idx == last_query:
        l, r = op[1], op[2]
        owed = [i for i in range(1, size) if lazy[i] != 0]
        if owed:
            pending = (
                f" Node{'s' if len(owed) != 1 else ''} {', '.join(str(i) for i in owed)} "
                f"hold{'' if len(owed) != 1 else 's'} a pending tag."
            )
        else:
            pending = " No node holds a pending tag."
        pushes.clear()
        recording = True
        step(
            f"Sum positions {l} up to, but not including, {r}, after the earlier updates."
            + pending + (" Leaves beneath a tag are not up to date yet." if owed else "")
        )
        answer = query(1, 0, size, l, r)
        states.clear()
        answers.append(answer)
        total = " + ".join(str(x) for x in reads)
        text = f"The answer is {total} = {answer}." if len(reads) > 1 else f"The answer is {answer}."
        if not pushes and owed:
            text += (
                f" No push was needed: the pending tag on node{'s' if len(owed) != 1 else ''} "
                f"{', '.join(str(i) for i in owed)} lies off the query's path, so it stays "
                "pending."
            )
        elif pushes:
            text += (
                f" The query pushed tags down from node{'s' if len(pushes) != 1 else ''} "
                f"{', '.join(str(i) for i in pushes)} only."
            )
        step(text)
        recording = False
    else:
        answers.append(query(1, 0, size, op[1], op[2]))

rec.output("\n".join(str(a) for a in answers) + "\n")
