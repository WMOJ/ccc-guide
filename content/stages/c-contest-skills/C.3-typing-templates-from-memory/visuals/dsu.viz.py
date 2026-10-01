import vizrec as vz

rec = vz.Recorder()
n, m = map(int, rec.readline().split())
unions = [tuple(map(int, rec.readline().split())) for _ in range(m)]
q = int(rec.readline())
queries = [tuple(map(int, rec.readline().split())) for _ in range(q)]

parent = list(range(n))
size = [1] * n


def find(x):
    """The template's find with path halving; also returns the parent cells it rewrote."""
    changed = []
    while parent[x] != x:
        old = parent[x]
        parent[x] = parent[parent[x]]
        if parent[x] != old:
            changed.append((x, old, parent[x]))
        x = parent[x]
    return x, changed


def layout():
    kids = [[] for _ in range(n)]
    for v in range(n):
        if parent[v] != v:
            kids[parent[v]].append(v)
    roots = [v for v in range(n) if parent[v] == v]
    leaves = sum(1 for v in range(n) if not kids[v])
    step = 1.5 if leaves <= 4 else 1.0
    pos = {}
    col = [0]

    def place(v, d):
        if not kids[v]:
            x = col[0] * step
            col[0] += 1
        else:
            xs = [place(c, d + 1) for c in kids[v]]
            x = sum(xs) / len(xs)
        pos[v] = (round(x, 2), round(d * 1.5, 2))
        return x

    for r in roots:
        place(r, 0)
    return pos


def frame(hot=(), moved=()):
    pos = layout()
    nodes = [(v, pos[v][0], pos[v][1]) for v in range(n)]
    edges = [(v, parent[v]) for v in range(n) if parent[v] != v]
    states = {v: "current" for v in hot}
    for v in moved:
        states[v] = "compare"
    values = {v: size[v] for v in range(n) if parent[v] == v}
    cell_states = ["_"] * n
    for v in hot:
        cell_states[v] = "c"
    for v in moved:
        cell_states[v] = "m"
    return {
        "arr": vz.array(parent, states="".join(cell_states), name="parent"),
        "forest": vz.graph(nodes, edges, node_states=states, values=values, directed=True, value_label="size"),
    }


rec.step(
    f"Start with {n} separate sets. Every node is its own root: parent[i] = i and size[i] = 1. "
    "An arrow leads from a node to its parent, and a root shows its size.",
    **frame(),
)
answers = []
for a, b in unions:
    ra, ca = find(a)
    rb, cb = find(b)
    moved = [x for x, _, _ in ca + cb]
    note = ""
    if moved:
        note = " Path halving rewrote " + ", ".join(f"parent[{x}] from {o} to {nw}" for x, o, nw in ca + cb) + "."
    if ra == rb:
        rec.step(
            f"union({a}, {b}): find({a}) and find({b}) both give root {ra}, so the two nodes are already in "
            f"one set and nothing changes.{note}",
            **frame([ra], moved),
        )
        continue
    if size[ra] < size[rb]:
        parent[ra] = rb
        size[rb] += size[ra]
        big, small = rb, ra
        why = f"size[{ra}] = {size[ra]} is less than size[{rb}]"
    else:
        parent[rb] = ra
        size[ra] += size[rb]
        big, small = ra, rb
        why = f"size[{ra}] is not less than size[{rb}]"
    rec.step(
        f"union({a}, {b}): find({a}) = {ra} and find({b}) = {rb} are different roots. {why}, so root {small} "
        f"goes under root {big}: parent[{small}] = {big}, and size[{big}] becomes {size[big]}.{note}",
        **frame([big], moved),
    )
for a, b in queries:
    ra, ca = find(a)
    rb, cb = find(b)
    moved = [x for x, _, _ in ca + cb]
    note = ""
    if moved:
        note = " Path halving rewrote " + ", ".join(f"parent[{x}] from {o} to {nw}" for x, o, nw in ca + cb) + "."
    word = "yes" if ra == rb else "no"
    same = "the same root" if ra == rb else "different roots"
    answers.append(word)
    rec.step(
        f"Query {a} and {b}: find({a}) = {ra} and find({b}) = {rb}, {same}. The answer is {word}.{note}",
        **frame([ra, rb], moved),
    )
rec.output("\n".join(answers) + "\n")
