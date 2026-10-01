import vizrec as vz

rec = vz.Recorder()
data = rec.stdin.split()
n = int(data[0])
K = int(data[1])
pos = 2
tri = []
for i in range(n):
    tri.append([int(x) for x in data[pos:pos + i + 1]])
    pos += i + 1

sizes = [1]
while sizes[-1] < K:
    m = sizes[-1]
    sizes.append(2 if m == 1 else min(K, 2 * m - 1))

levels = {1: tri}
for a, b in zip(sizes, sizes[1:]):
    off = b - a
    cur = levels[a]
    levels[b] = [[max(cur[i][j], cur[i + off][j], cur[i + off][j + off]) for j in range(i + 1)]
                 for i in range(n - b + 1)]
final = levels[sizes[-1]]


def panel(level, states=None, only=None):
    """level: rows of a size-m table. only: set of cells to show (others blank)."""
    cells = []
    vals = []
    for i in range(n):
        crow = ""
        vrow = []
        for j in range(n):
            ok = j <= i and i < len(level)
            if not ok:
                crow += "#"
                vrow.append(None)
            else:
                crow += vz.code((states or {}).get((i, j)))
                vrow.append(level[i][j] if only is None or (i, j) in only else None)
        cells.append(crow)
        vals.append(vrow)
    return vz.grid(cells, values=vals)


def count(s):
    return (n - s + 1) * (n - s + 2) // 2


ladder = ", ".join(map(str, sizes))
if K == 1:
    rec.step(
        f"A triangle of {n} rows. A size-1 triangle is a single cell, so the answer is the triangle "
        "itself and nothing has to be built.",
        a=panel(tri),
        b=panel(tri),
    )
else:
    rec.step(
        f"A triangle of {n} rows, one cell per apex. Each cell holds the maximum of its own size-1 "
        f"triangle. To reach size {K}, the sizes built are {ladder}. The right panel will hold each "
        "new size.",
        a=panel(tri),
        b=panel(levels[sizes[1]], only=set()),
    )
for a, b in zip(sizes, sizes[1:]):
    off = b - a
    cur = levels[a]
    new = levels[b]
    i = min(1, n - b)
    j = 0
    trio = [(i, j), (i + off, j), (i + off, j + off)]
    vals = [cur[r][c] for r, c in trio]
    best = new[i][j]
    if a == 1:
        why = "The first step is special: a size-2 triangle is three cells, which are three size-1 triangles."
    else:
        why = f"Size {b} is at most 2 * {a} - 1 = {2 * a - 1}, so three triangles of size {a} cover it."
    rec.step(
        f"Size {b} from size {a}. The size-{b} triangle at apex ({i}, {j}) is covered by the size-{a} "
        f"triangles at ({trio[0][0]}, {trio[0][1]}), ({trio[1][0]}, {trio[1][1]}) and "
        f"({trio[2][0]}, {trio[2][1]}), whose maxima are {vals[0]}, {vals[1]} and {vals[2]}. "
        f"The maximum is {best}. {why}",
        a=panel(cur, {t: "compare" for t in trio}),
        b=panel(new, {(i, j): "current"}, only={(i, j)}),
    )
    rec.step(
        f"The same three lookups fill {'the only apex' if count(b) == 1 else 'all ' + str(count(b)) + ' apexes'} "
        f"of size {b}. Each one costs one max of three values, however large the triangle is.",
        a=panel(cur),
        b=panel(new, {(r, c): "done" for r in range(len(new)) for c in range(r + 1)}),
    )
text = "\n".join(" ".join(map(str, row)) for row in final)
rec.step(
    f"The size-{K} triangles have these maxima, one row per apex row: "
    + "; ".join(" ".join(map(str, row)) for row in final)
    + ".",
    a=panel(tri),
    b=panel(final, {(r, c): "done" for r in range(len(final)) for c in range(r + 1)}),
)
rec.output(text + "\n")
