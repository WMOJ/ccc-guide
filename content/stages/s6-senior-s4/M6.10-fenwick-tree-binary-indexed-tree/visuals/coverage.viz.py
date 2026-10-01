import vizrec as vz

rec = vz.Recorder()
data = rec.stdin.split()
n = int(data[0])
values = [int(v) for v in data[1:n + 1]]
width = n.bit_length()
tree = [None] * n


def value_frame(start=None, end=None, label=None):
    states = ["none"] * n
    ranges = None
    if start is not None:
        for k in range(start - 1, end):
            states[k] = "current"
        ranges = [(start - 1, end - 1, label)]
    return vz.array(values, states=states, ranges=ranges, index_base=1)


def tree_frame(at=None):
    states = ["done" if tree[k] is not None else "none" for k in range(n)]
    pointers = None
    if at is not None:
        states[at - 1] = "current"
        pointers = {"i": at - 1}
    return vz.array(tree, states=states, pointers=pointers, index_base=1)


rec.step(
    f"{n} elements sit in positions 1 to {n}. The tree below them starts unfilled. Each tree "
    "position will hold the sum of a block of elements that ends at that position.",
    values=value_frame(),
    tree=tree_frame(),
)

lines = []
for i in range(1, n + 1):
    low = i & -i
    start = i - low + 1
    total = sum(values[start - 1:i])
    bits = bin(i)[2:].zfill(width)
    tree[i - 1] = total
    if low == 1:
        where = f"tree[{i}] covers just position {i}."
    else:
        where = f"tree[{i}] covers {low} elements ending at {i}: positions {start} to {i}."
    rec.step(
        f"Position {i} is {bits} in binary. Its lowest set bit is {low}, so {where} "
        f"The sum is {total}.",
        values=value_frame(start, i, f"tree[{i}]"),
        tree=tree_frame(i),
    )
    lines.append(f"{i} {bits} {low} {start}..{i} {total}")

rec.step(
    "The tree is full. A position with a higher lowest set bit covers a longer block, so most "
    "positions hold short blocks and only a few hold long ones.",
    values=value_frame(),
    tree=tree_frame(),
)
rec.output("\n".join(lines) + "\n")
