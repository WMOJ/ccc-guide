import vizrec as vz

rec = vz.Recorder()
n = int(rec.readline())
values = [int(x) for x in rec.readline().split()]

size = 1
while size < n:
    size *= 2

tree = [0] * (2 * size)
for i in range(n):
    tree[size + i] = values[i]
known = set(range(size, 2 * size))


def real(i):
    k = i
    while k < size:
        k *= 2
    return k - size < n


def build(i, states):
    kids = None
    if i < size:
        kids = [build(c, states) for c in (2 * i, 2 * i + 1) if real(c)]
    label = tree[i] if i in known else "?"
    return vz.node(i, label, children=kids, state=states.get(i), note=f"#{i}")


def frame(states=None):
    return {"t": vz.tree(build(1, states or {}))}


if size > n:
    first = (
        f"The {n} values sit in the leaves `tree[{size}]` to `tree[{size + n - 1}]`. The "
        f"remaining {size - n} leaves are padding that hold 0 and are not drawn, and neither "
        "is any node above only padding. Every drawn internal node is still unknown (?)."
    )
else:
    first = (
        f"The {n} values sit in the leaves, `tree[{size}]` to `tree[{2 * size - 1}]`. Every "
        "internal node is still unknown (?)."
    )
rec.step(first, **frame())

for i in range(size - 1, 0, -1):
    left, right = tree[2 * i], tree[2 * i + 1]
    tree[i] = left + right
    known.add(i)
    if not real(i):
        continue
    if real(2 * i + 1):
        rec.step(
            f"`tree[{i}] = tree[{2 * i}] + tree[{2 * i + 1}]`, so {left} + {right} = {tree[i]}.",
            **frame({i: "current", 2 * i: "compare", 2 * i + 1: "compare"})
        )
    else:
        rec.step(
            f"`tree[{i}] = tree[{2 * i}] + tree[{2 * i + 1}]`, and `tree[{2 * i + 1}]` is "
            f"padding (0, not drawn), so {left} + 0 = {tree[i]}.",
            **frame({i: "current", 2 * i: "compare"})
        )

rec.step(
    f"Every internal node is filled in. The root `tree[1]` is {tree[1]}, the sum of the whole "
    "array, and each node holds the sum of the leaves beneath it.",
    **frame({1: "done"})
)
rec.output(f"size {size}\ntree {tree}\n")
