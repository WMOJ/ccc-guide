import vizrec as vz

rec = vz.Recorder()
n = int(rec.readline())
a = list(map(int, rec.readline().split()))

LOG = n.bit_length()
sp = [a]
for k in range(1, LOG):
    prev = sp[k - 1]
    half = 1 << (k - 1)
    sp.append([min(prev[i], prev[i + half]) for i in range(n - (1 << k) + 1)])

heads = [f"sp[{k}]" for k in range(LOG)]
filled = [[False] * LOG for _ in range(n)]
for i in range(n):
    filled[i][0] = True


def cell(i, k):
    if filled[i][k]:
        return sp[k][i]
    return "-"


def frame(compare=(), current=None):
    cells = [[cell(i, k) for k in range(LOG)] for i in range(n)]
    states = {}
    for i in range(n):
        for k in range(LOG):
            if filled[i][k]:
                states[(i, k)] = "done"
    for c in compare:
        states[c] = "compare"
    if current is not None:
        states[current] = "current"
    return vz.table(cells, states=states, row_heads=list(range(n)), col_heads=heads, row_title="i")


rec.step(
    "Column sp[0] is the array: sp[0][i] is the smallest value in the block of length 1 that starts "
    "at i. The other columns are empty (-).",
    table=frame(),
)
for k in range(1, LOG):
    half = 1 << (k - 1)
    size = 1 << k
    for i in range(n - size + 1):
        x = sp[k - 1][i]
        y = sp[k - 1][i + half]
        filled[i][k] = True
        rec.step(
            f"sp[{k}][{i}] = min(sp[{k - 1}][{i}], sp[{k - 1}][{i + half}]) = min({x}, {y}) = {sp[k][i]}. "
            f"The block of length {size} starting at {i} is two blocks of length {half}, "
            f"starting at {i} and {i + half}.",
            table=frame(compare=[(i, k - 1), (i + half, k - 1)], current=(i, k)),
        )
last = LOG - 1
if last == 0:
    rec.step("With one element there is only level 0.", table=frame())
else:
    rec.step(
        f"The table is full. A dash means no block of that length starts there, because it would run "
        f"past the end of the array. The largest block is sp[{last}][0] = {sp[last][0]}, the minimum of "
        f"the first {1 << last} elements.",
        table=frame(),
    )
rec.output("".join(f"sp[{k}] = {sp[k]}\n" for k in range(LOG)))
