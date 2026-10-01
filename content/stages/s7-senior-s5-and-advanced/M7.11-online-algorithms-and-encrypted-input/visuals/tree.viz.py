import vizrec as vz

rec = vz.Recorder()
n = int(rec.readline())
values = [int(x) for x in rec.readline().split()]
q = int(rec.readline())
lines = [tuple(int(t) for t in rec.readline().split()) for _ in range(q)]

size = 1
while size < n:
    size *= 2
tree = [0] * (2 * size)
for i in range(n):
    tree[size + i] = values[i]
for i in range(size - 1, 0, -1):
    tree[i] = tree[2 * i] + tree[2 * i + 1]


def real(i):
    k = i
    while k < size:
        k *= 2
    return k - size < n


def build(i, states):
    kids = None
    if i < size:
        kids = [build(c, states) for c in (2 * i, 2 * i + 1) if real(c)]
    return vz.node(i, tree[i], children=kids, state=states.get(i), note=f"#{i}")


def frame(states, last, action, result):
    return {
        "t": vz.tree(build(1, states)),
        "v": vz.table([[last, action, result]], col_heads=["last", "decoded", "result"]),
    }


rec.step(
    f"The tree of M7.1 for {values}, built before any line is read. Its root `tree[1]` holds "
    f"{tree[1]}. Each of the {q} lines will be decoded with `last`, then answered on this tree.",
    **frame({}, 0, "-", "-")
)
last = 0
results = []
for i, (kind, x, y) in enumerate(lines):
    if kind == 1:
        p = (x + last) % n
        v = (y + last) % 100
        leaf = size + p
        old = tree[leaf]
        tree[leaf] = v
        path = [leaf]
        k = leaf // 2
        while k >= 1:
            tree[k] = tree[2 * k] + tree[2 * k + 1]
            path.append(k)
            k //= 2
        states = {k: "current" for k in path}
        rec.step(
            f"Line {i + 1}, `{kind} {x} {y}`, with `last` = {last} decodes to: set position {p} "
            f"to {v}. The leaf `tree[{leaf}]` changes from {old} to {v}, and its ancestors "
            f"{', '.join(str(k) for k in path[1:])} are recomputed, one per level. Nothing is "
            "answered, so `last` stays.",
            **frame(states, last, f"a[{p}]={v}", "-")
        )
    else:
        f = (x + last) % n
        s = (y + last) % n
        lo0, hi0 = min(f, s), max(f, s)
        lo = lo0 + size
        hi = hi0 + 1 + size
        taken = []
        total = 0
        while lo < hi:
            if lo % 2 == 1:
                taken.append(lo)
                total += tree[lo]
                lo += 1
            if hi % 2 == 1:
                hi -= 1
                taken.append(hi)
                total += tree[hi]
            lo //= 2
            hi //= 2
        states = {k: "done" for k in taken}
        nodes = " + ".join(f"{tree[k]} (node {k})" for k in taken)
        count = len(taken)
        rec.step(
            f"Line {i + 1}, `{kind} {x} {y}`, with `last` = {last} decodes to: sum positions "
            f"{lo0} to {hi0}. The query loop of M7.1 takes {count} node{'s' if count != 1 else ''}: "
            f"{nodes} = {total}. This answer becomes `last`.",
            **frame(states, last, f"sum {lo0}-{hi0}", total)
        )
        last = total
        results.append(str(total))
rec.step(
    f"The last answer is {last}. The tree did the same work as in M7.1. The only new lines are "
    "the ones that decode each line with `last`.",
    **frame({}, last, "-", "-")
)
rec.output("\n".join(results) + "\n")
