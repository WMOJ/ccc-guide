import vizrec as vz

rec = vz.Recorder()
data = rec.stdin.split()
n = int(data[0])
grid = [[int(data[1 + i * n + j]) for j in range(n)] for i in range(n)]
pos = 1 + n * n
q = int(data[pos])
pos += 1
queries = []
for _ in range(q):
    queries.append((int(data[pos]), int(data[pos + 1]), int(data[pos + 2])))
    pos += 3

table = [grid]
for k in range(1, n.bit_length()):
    half = 1 << (k - 1)
    prev = table[k - 1]
    span = n - (1 << k) + 1
    table.append([[max(prev[i][j], prev[i][j + half], prev[i + half][j], prev[i + half][j + half])
                   for j in range(span)] for i in range(span)])


def panel(values, states=None):
    size = len(values)
    st = ["".join(vz.code((states or {}).get((i, j))) for j in range(size)) for i in range(size)]
    return vz.grid(st, values=values)


def blank_of(size, done):
    return [[done[i][j] if (i, j) in done else None for j in range(size)] for i in range(size)]


rec.step(
    f"Level 0 is the {n} by {n} grid itself: every cell is the maximum of its own 1 by 1 block. "
    "Each later level is built from the level before it.",
    src=panel(grid),
    dst=panel([[None] * (n - 1) for _ in range(n - 1)]),
)
for k in range(1, n.bit_length()):
    half = 1 << (k - 1)
    size = 1 << k
    prev = table[k - 1]
    span = len(table[k])
    made = {}
    src_size = len(prev)
    for i in range(span):
        for j in range(span):
            cells = [(i, j), (i, j + half), (i + half, j), (i + half, j + half)]
            vals = [prev[a][b] for a, b in cells]
            made[(i, j)] = table[k][i][j]
            src_states = {c: "compare" for c in cells}
            dst_vals = [[made.get((a, b)) for b in range(span)] for a in range(span)]
            dst_states = {c: "done" for c in made}
            dst_states[(i, j)] = "current"
            if k == 1:
                where = (f"The block at rows {i} to {i + 1} and columns {j} to {j + 1} holds "
                         f"{', '.join(map(str, vals))}.")
            else:
                where = (f"The {size} by {size} block at row {i}, column {j} is four level-{k - 1} "
                         f"blocks of side {half}, at offsets 0 and {half} in each direction.")
            rec.step(
                f"Level {k}, cell ({i}, {j}). {where} Its maximum is "
                f"max({', '.join(map(str, vals))}) = {table[k][i][j]}.",
                src=panel(prev, src_states),
                dst=panel(dst_vals, dst_states),
            )
    last = table[k]
    rec.step(
        f"Level {k} is complete: a {span} by {span} table, one cell for each {size} by {size} block "
        f"that fits in the grid.",
        src=panel(prev),
        dst=panel(last, {(a, b): "done" for a in range(span) for b in range(span)}),
    )

out = []
for r, c, s in queries:
    k = s.bit_length() - 1
    far = s - (1 << k)
    t = table[k]
    out.append(max(t[r][c], t[r][c + far], t[r + far][c], t[r + far][c + far]))
r, c, s = queries[0]
k = s.bit_length() - 1
far = s - (1 << k)
t = table[k]
cells = [(r, c), (r, c + far), (r + far, c), (r + far, c + far)]
vals = [t[a][b] for a, b in cells]
if far == 0:
    text = (f"The whole {n} by {n} grid is one block of side {s} at level {k}, so the four lookups "
            f"are the same cell. The answer is {out[0]}.")
else:
    text = (f"The whole {n} by {n} grid has side {s}. The largest power of two that fits is "
            f"{1 << k}, so four level-{k} blocks, at offsets 0 and {far}, cover it. Their maximum "
            f"is max({', '.join(map(str, vals))}) = {out[0]}.")
rec.step(
    text,
    src=panel(t, {c_: "compare" for c_ in cells}),
    dst=panel([[out[0]]], {(0, 0): "done"}),
)
rec.output("\n".join(map(str, out)) + "\n")
