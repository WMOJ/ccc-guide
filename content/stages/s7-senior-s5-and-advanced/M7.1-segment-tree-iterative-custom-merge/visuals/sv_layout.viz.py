import vizrec as vz

rec = vz.Recorder()
n = int(rec.readline())
values = [int(x) for x in rec.readline().split()]
mode, arg = rec.readline().split()
arg = int(arg)

size = 1
while size < n:
    size *= 2
tree = [0] * (2 * size)
for i in range(n):
    tree[size + i] = values[i]
for i in range(size - 1, 0, -1):
    tree[i] = tree[2 * i] + tree[2 * i + 1]


def build(i, states):
    kids = None
    if i < size:
        kids = [build(2 * i, states), build(2 * i + 1, states)]
    return vz.node(i, tree[i], children=kids, state=states.get(i), note=f"#{i}")


def frame(states):
    cells = ["-"] + tree[1:]
    return {
        "t": vz.tree(build(1, states)),
        "a": vz.array(cells, states={i: s for i, s in states.items()}),
    }


if mode == "up":
    i = size + arg
    rec.step(
        f"The value at position {arg} lives in a leaf. Its index is `size + {arg}`, so "
        f"{size} + {arg} = {i}: `tree[{i}]` holds {tree[i]}. The same cell is marked in the tree "
        "and in the list.",
        **frame({i: "current"})
    )
    seen = {}
    while i > 1:
        seen[i] = "done"
        parent = i // 2
        states = dict(seen)
        states[parent] = "current"
        rec.step(
            f"The parent of node {i} is {i} // 2 = {parent}. Node {parent} holds {tree[parent]}, "
            f"the sum of everything beneath it.",
            **frame(states)
        )
        i = parent
    final = dict(seen)
    final[1] = "current"
    rec.step(
        "The next step would be 1 // 2 = 0, which is not a node (index 0 is never used). "
        "The walk stops at the root: each leaf is at most log2(size) halvings from it.",
        **frame(final)
    )
else:
    rec.step(
        "Start at the root, node 1. Its children are at indices 2 * 1 = 2 and 2 * 1 + 1 = 3, "
        "the two halves of the array.",
        **frame({1: "current", 2: "compare", 3: "compare"})
    )
    rec.step(
        "Take node 3 and double again: its children are 2 * 3 = 6 and 2 * 3 + 1 = 7. These "
        "are the last two leaves, positions 2 and 3.",
        **frame({1: "done", 3: "current", 6: "compare", 7: "compare"})
    )
    rec.step(
        f"Node 6 is a leaf. Its would-be children, 2 * 6 = 12 and 13, are past the end of the "
        f"list, which has {2 * size} entries (indices 0 to {2 * size - 1}). Leaves are exactly "
        f"the indices {size} and up.",
        **frame({1: "done", 3: "done", 6: "current"})
    )

rec.output(f"size {size}\ntree {tree}\n")
