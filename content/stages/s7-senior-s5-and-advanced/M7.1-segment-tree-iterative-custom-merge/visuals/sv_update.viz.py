import vizrec as vz

rec = vz.Recorder()
n = int(rec.readline())
values = [int(x) for x in rec.readline().split()]
rec.readline()
_, pos, new_value = map(int, rec.readline().split())

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


def frame(states):
    return {"t": vz.tree(build(1, states))}


i = size + pos
old = tree[i]
rec.step(
    f"Change position {pos} from {old} to {new_value}. Its leaf is `tree[{size} + {pos}]`, "
    f"which is `tree[{i}]`. The root says {tree[1]} for the whole array.",
    **frame({i: "current"})
)

ancestors = []
k = i // 2
while k >= 1:
    ancestors.append(k)
    k //= 2
tree[i] = new_value
stale = {a: "path" for a in ancestors}
stale[i] = "current"
rec.step(
    f"Write {new_value} into `tree[{i}]`. Each ancestor ({', '.join(str(a) for a in ancestors)}) "
    "still holds a sum that includes the old value, so all of them are stale.",
    **frame(stale)
)
while ancestors:
    k = ancestors.pop(0)
    before = tree[k]
    tree[k] = tree[2 * k] + tree[2 * k + 1]
    states = {a: "path" for a in ancestors}
    states[k] = "current"
    states[2 * k] = "compare"
    states[2 * k + 1] = "compare"
    rec.step(
        f"`tree[{k}] = tree[{2 * k}] + tree[{2 * k + 1}]` = {tree[2 * k]} + {tree[2 * k + 1]} "
        f"= {tree[k]}, replacing {before}.",
        **frame(states)
    )

rec.step(
    f"Only {len(stale)} nodes changed, one per level. The total of all the values is the "
    f"root, `tree[1]` = {tree[1]}.",
    **frame({1: "done"})
)
rec.output(f"{tree[1]}\n")
