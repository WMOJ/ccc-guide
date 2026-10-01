import vizrec as vz

rec = vz.Recorder()
data = rec.stdin.split()
n = int(data[0])
values = [int(v) for v in data[1:n + 1]]
pos = n + 2
p = int(data[pos + 1])
delta = int(data[pos + 2])


def build_prefix(vals):
    prefix = [0]
    for v in vals:
        prefix.append(prefix[-1] + v)
    return prefix


def build_tree(vals):
    tree = [0] * (n + 1)
    for i in range(1, n + 1):
        low = i & -i
        tree[i] = sum(vals[i - low:i])
    return tree[1:]


prefix = build_prefix(values)
tree = build_tree(values)
rec.step(
    f"The same {n} elements, stored two ways. prefix[i] is the total of the first i elements, "
    "with prefix[0] = 0. Each tree[i] is the total of a block that ends at i.",
    prefix=vz.array(prefix, index_base=0),
    tree=vz.array(tree, index_base=1),
)

values[p - 1] += delta
new_prefix = build_prefix(values)
changed = [k for k in range(n + 1) if new_prefix[k] != prefix[k]]
rec.step(
    f"Element {p} goes up by {delta}. Every prefix entry from prefix[{p}] to prefix[{n}] includes "
    f"that element, so all {len(changed)} of them must be rewritten. The earlier the "
    "position, the more entries: at position 1 with 100,000 elements, all 100,000 entries.",
    prefix=vz.array(new_prefix, states={k: "current" for k in changed}, index_base=0),
    tree=vz.array(tree, index_base=1),
)

new_tree = build_tree(values)
touched = [k for k in range(n) if new_tree[k] != tree[k]]
names = ", ".join(f"tree[{k + 1}]" for k in touched)
rec.step(
    f"The Fenwick tree rewrites only the blocks that contain position {p}: {names}. That is "
    f"{len(touched)} of {n} entries. For 100,000 elements no update touches more than 17.",
    prefix=vz.array(new_prefix, index_base=0),
    tree=vz.array(new_tree, states={k: "current" for k in touched}, index_base=1),
)
rec.output(f"{sum(values)}\n")
