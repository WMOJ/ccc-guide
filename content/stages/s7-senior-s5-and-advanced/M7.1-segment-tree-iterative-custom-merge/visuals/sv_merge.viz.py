import vizrec as vz

NEG = -10 ** 18
IDENTITY = (0, NEG, NEG, NEG)

rec = vz.Recorder()
n = int(rec.readline())
values = [int(x) for x in rec.readline().split()]
rec.readline()
_, left, right = map(int, rec.readline().split())


def merge(a, b):
    total = a[0] + b[0]
    best_prefix = max(a[1], a[0] + b[1])
    best_suffix = max(b[2], b[0] + a[2])
    best_inside = max(a[3], b[3], a[2] + b[1])
    return (total, best_prefix, best_suffix, best_inside)


size = 1
while size < n:
    size *= 2
tree = [IDENTITY] * (2 * size)
for i in range(n):
    v = values[i]
    tree[size + i] = (v, v, v, v)
for i in range(size - 1, 0, -1):
    tree[i] = merge(tree[2 * i], tree[2 * i + 1])


def shown(t):
    return [("-" if x <= NEG // 2 else x) for x in t]


def span(k):
    width = 1
    while k < size:
        k *= 2
        width *= 2
    first = k - size
    if width == 1:
        return f"position {first}"
    return f"positions {first} to {first + width - 1}"


def frame(left_part, right_part, node=None, merged=None):
    blank = ["", "", "", ""]
    rows = [
        shown(left_part),
        shown(right_part),
        shown(node) if node else blank,
        shown(merged) if merged else blank,
    ]
    states = {}
    for c in range(4):
        if node:
            states[(2, c)] = "current"
        if merged:
            states[(3, c)] = "done"
    return {
        "v": vz.table(rows, states=states or None,
                      row_heads=["left_part", "right_part", "node", "merged"],
                      col_heads=["total", "prefix", "suffix", "inside"])
    }


def why(a, b, result):
    cands = [("left's best", a[3]), ("right's best", b[3]), ("a run across the boundary", a[2] + b[1])]
    if a == IDENTITY or b == IDENTITY:
        return "One side is the identity, so the merge just copies the other side."
    winner = [name for name, val in cands if val == result[3]][0]
    return (
        f"The best `inside` is the largest of left's best ({a[3]}), right's best ({b[3]}), "
        f"and a run across the boundary, suffix {a[2]} + prefix {b[1]} = {a[2] + b[1]}. "
        f"Winner: {winner}, {result[3]}."
    )


left_part = IDENTITY
right_part = IDENTITY
rec.step(
    "Each node holds four numbers: `total`, the best `prefix` (a run starting at its left end), "
    "the best `suffix`, and the best run `inside`. A dash means no run exists yet. Both parts "
    f"start as the identity. The query covers positions {left} up to, but not including, "
    f"{right}.",
    **frame(left_part, right_part)
)
lo = left + size
hi = right + size
while lo < hi:
    if lo % 2 == 1:
        node = tree[lo]
        result = merge(left_part, node)
        a, b = left_part, node
        rec.step(
            f"`lo` = {lo} is odd: merge `left_part` with `tree[{lo}]` ({span(lo)}), "
            f"in that order. {why(a, b, result)}",
            **frame(left_part, right_part, node, result)
        )
        left_part = result
        lo += 1
    if hi % 2 == 1:
        hi -= 1
        node = tree[hi]
        result = merge(node, right_part)
        a, b = node, right_part
        rec.step(
            f"`hi` is odd: merge `tree[{hi}]` ({span(hi)}) "
            f"with `right_part`, with the node on the left. {why(a, b, result)}",
            **frame(left_part, right_part, node, result)
        )
        right_part = result
    lo //= 2
    hi //= 2

answer = merge(left_part, right_part)
rec.step(
    f"The loop is done. Merging `left_part` and `right_part` gives the final node. "
    f"{why(left_part, right_part, answer)} The answer is its `inside` number, {answer[3]}.",
    **frame(left_part, right_part, None, answer)
)
rec.output(f"{answer[3]}\n")
