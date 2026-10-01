import vizrec as vz

rec = vz.Recorder()
data = rec.stdin.split()
n = int(data[0])
values = [int(v) for v in data[1:n + 1]]
tree = [0] * (n + 1)
for i in range(1, n + 1):
    low = i & -i
    tree[i] = sum(values[i - low:i])
bits_w = n.bit_length()
kind = data[n + 2]
left = int(data[n + 3])
right = int(data[n + 4])


def value_frame(added, current=None, span=None):
    states = ["none"] * n
    for k in added:
        states[k - 1] = "done"
    ranges = None
    if current is not None:
        for k in range(current[0], current[1] + 1):
            states[k - 1] = "current"
        ranges = [(current[0] - 1, current[1] - 1, f"tree[{current[2]}]")]
    elif span is not None:
        ranges = [(span[0] - 1, span[1] - 1, f"query {span[0]}-{span[1]}")]
    return vz.array(values, states=states, ranges=ranges, index_base=1)


def tree_frame(visited, at=None):
    states = ["none"] * n
    for k in visited:
        states[k - 1] = "done"
    pointers = None
    if at is not None and at >= 1:
        states[at - 1] = "current"
        pointers = {"i": at - 1}
    return vz.array(tree[1:], states=states, pointers=pointers, index_base=1)


def span_text(a, b):
    if a == b:
        return f"position {a}"
    return f"positions {a} to {b}"


def prefix_text(k):
    if k == 0:
        return "nothing"
    return span_text(1, k)


def binary(v):
    return bin(v)[2:].zfill(bits_w)


rec.step(
    f"The sum of {span_text(left, right)} is query({right}) minus query({left - 1}): the "
    f"total of {prefix_text(right)}, minus the total of {prefix_text(left - 1)}. "
    "query(i) adds tree entries while it walks i down to 0.",
    values=value_frame([], span=(left, right)),
    tree=tree_frame([]),
)


def walk(start, label):
    i = start
    added = []
    visited = []
    total = 0
    if i == 0:
        rec.step(
            "query(0) starts at 0, so the loop body never runs and the result is 0. "
            f"Nothing lies before position {left}.",
            values=value_frame([]),
            tree=tree_frame([]),
        )
        return 0
    while i > 0:
        low = i & -i
        lo = i - low + 1
        total += tree[i]
        nxt = i - low
        rec.step(
            f"{label}: i is {i} ({binary(i)}). Add tree[{i}] = {tree[i]}, the sum of "
            f"{span_text(lo, i)}. The total is {total}. Remove the lowest set bit, {low}, to reach "
            f"i = {nxt} ({binary(nxt)}).",
            values=value_frame(added, current=(lo, i, i)),
            tree=tree_frame(visited, at=i),
        )
        added.extend(range(lo, i + 1))
        visited.append(i)
        i = nxt
    rec.step(
        f"i reached 0, so {label} stops with {total}, the sum of {prefix_text(start)}.",
        values=value_frame(added),
        tree=tree_frame(visited),
    )
    return total


upper = walk(right, f"query({right})")
lower = walk(left - 1, f"query({left - 1})")
result = upper - lower
rec.step(
    f"The range sum is {upper} - {lower} = {result}, the total of {span_text(left, right)}.",
    values=value_frame([], span=(left, right)),
    tree=tree_frame([]),
)
rec.output(f"{result}\n")
