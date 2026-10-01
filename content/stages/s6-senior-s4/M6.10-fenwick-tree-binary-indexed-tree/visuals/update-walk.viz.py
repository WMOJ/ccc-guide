import vizrec as vz

rec = vz.Recorder()
data = rec.stdin.split()
n = int(data[0])
values = [int(v) for v in data[1:n + 1]]
tree = [0] * (n + 1)
for i in range(1, n + 1):
    low = i & -i
    tree[i] = sum(values[i - low:i])
bits_w = (2 * n).bit_length()
pos = n + 2
p = int(data[pos + 1])
delta = int(data[pos + 2])


def binary(v):
    return bin(v)[2:].zfill(bits_w)


def value_frame(rng=None):
    states = ["none"] * n
    states[p - 1] = "current"
    ranges = None
    if rng is not None:
        ranges = [(rng[0] - 1, rng[1] - 1, f"tree[{rng[2]}]")]
    return vz.array(values, states=states, ranges=ranges, index_base=1)


def tree_frame(visited, at=None):
    states = ["none"] * n
    for k in visited:
        states[k - 1] = "done"
    pointers = None
    if at is not None:
        if at <= n:
            states[at - 1] = "current"
        pointers = {"i": min(at, n) - 1}
    return vz.array(tree[1:], states=states, pointers=pointers, index_base=1)


rec.step(
    f"Position {p} is about to go up by {delta}, from {values[p - 1]} to {values[p - 1] + delta}. "
    f"Every tree entry whose block contains position {p} must go up by {delta} too. "
    "The update finds them by starting at i and adding the lowest set bit.",
    values=value_frame(),
    tree=tree_frame([]),
)
values[p - 1] += delta

visited = []
i = p
while i <= n:
    low = i & -i
    lo = i - low + 1
    old = tree[i]
    tree[i] += delta
    nxt = i + low
    if nxt <= n:
        tail = f"Add the lowest set bit, {low}, to reach i = {nxt} ({binary(nxt)})."
    else:
        tail = f"Add the lowest set bit, {low}, to reach i = {nxt} ({binary(nxt)}), which is past {n}."
    if lo == i:
        block = f"tree[{i}] covers just position {i}"
    else:
        block = f"tree[{i}] covers positions {lo} to {i}, which include position {p}"
    rec.step(
        f"i is {i} ({binary(i)}). {block}, so it goes from {old} to {tree[i]}. {tail}",
        values=value_frame((lo, i, i)),
        tree=tree_frame(visited, at=i),
    )
    visited.append(i)
    i = nxt

rec.step(
    f"i is past {n}, so the update stops after {len(visited)} "
    f"{'entry' if len(visited) == 1 else 'entries'}. Every block that contained position {p} "
    f"now includes the change, and the {n} elements total {sum(values)}.",
    values=value_frame(),
    tree=tree_frame(visited),
)
rec.output(f"{sum(values)}\n")
