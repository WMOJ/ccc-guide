import vizrec as vz

rec = vz.Recorder()
n = int(rec.readline())
values = [int(x) for x in rec.readline().split()]
rec.readline()
left, right = map(int, rec.readline().split())

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


def frame(taken, lo, hi, left_part, right_part, pointers=True):
    states = {}
    for t in taken:
        states[t] = "done"
    if pointers and lo < hi:
        states[lo] = "current"
        states[hi] = "compare"
    return {
        "t": vz.tree(build(1, states)),
        "v": vz.table([[lo, hi, left_part, right_part]],
                      col_heads=["lo", "hi", "left_part", "right_part"]),
    }


lo = left + size
hi = right + size
taken = []
left_part = 0
right_part = 0
tail = ""
if hi >= size + n:
    tail = " (Node `hi` would be padding past the last value, so none is marked.)"
rec.step(
    f"Sum positions {left} up to, but not including, {right}. Add `size` ({size}) to both ends: "
    f"`lo` = {left} + {size} = {lo} and `hi` = {right} + {size} = {hi}. The nodes from `lo` up "
    "to, but not including, `hi` are the leaves in the range." + tail,
    **frame(taken, lo, hi, left_part, right_part)
)
while lo < hi:
    took = False
    if lo % 2 == 1:
        took = True
        left_part = left_part + tree[lo]
        taken.append(lo)
        if lo == 1:
            why = "`lo` = 1 is the root, and its range is exactly the query range."
        else:
            why = (
                f"`lo` = {lo} is odd, so it is a right child: its parent would also cover a "
                "leaf to the left of the range."
            )
        rec.step(
            f"{why} Take `tree[{lo}]` = {tree[lo]} into `left_part`, which is now "
            f"{left_part}. Then `lo` becomes {lo + 1}.",
            **frame(taken, lo + 1, hi, left_part, right_part, pointers=False)
        )
        lo += 1
    if hi % 2 == 1:
        took = True
        hi -= 1
        right_part = tree[hi] + right_part
        taken.append(hi)
        rec.step(
            f"`hi` is odd, so node {hi} (the one just before it) is a left child whose parent "
            f"would reach past the range. Take `tree[{hi}]` = {tree[hi]} into `right_part`, "
            f"which is now {right_part}. Then `hi` becomes {hi}.",
            **frame(taken, lo, hi, left_part, right_part, pointers=False)
        )
    lo //= 2
    hi //= 2
    if took:
        move = f"Both indices halve, moving up a level: `lo` = {lo}, `hi` = {hi}."
    else:
        move = (
            f"`lo` and `hi` are both even, so no node is taken at this level. Both halve: "
            f"`lo` = {lo}, `hi` = {hi}."
        )
    if lo < hi:
        rec.step(move, **frame(taken, lo, hi, left_part, right_part))
    else:
        rec.step(
            move + " `lo` has caught up with `hi`, so the loop stops.",
            **frame(taken, lo, hi, left_part, right_part)
        )

answer = left_part + right_part
rec.step(
    f"The query is `left_part + right_part` = {left_part} + {right_part} = {answer}. It used "
    f"{len(taken)} node{'s' if len(taken) != 1 else ''} instead of {right - left} "
    f"{'leaf' if right - left == 1 else 'leaves'}.",
    **frame(taken, lo, hi, left_part, right_part)
)
rec.output(f"{answer}\n")
