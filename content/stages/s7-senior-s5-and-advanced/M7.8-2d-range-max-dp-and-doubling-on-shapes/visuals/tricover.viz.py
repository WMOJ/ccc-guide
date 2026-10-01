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
m = sizes[-2]
off = K - m


def tri_cells(a, b, size):
    return {(a + r, b + c) for r in range(size) for c in range(r + 1)}


def tmax(a, b, size):
    return max(tri[i][j] for i, j in tri_cells(a, b, size))


corners = [(0, 0), (off, 0), (off, off)]
names = ["top", "bottom-left", "bottom-right"]
whole = tri_cells(0, 0, K)


def frame(upto):
    hits = {}
    for a, b in corners[:upto]:
        for cell in tri_cells(a, b, m):
            hits[cell] = hits.get(cell, 0) + 1
    cells = []
    for i in range(n):
        row = ""
        for j in range(n):
            if j > i:
                row += "#"
            elif hits.get((i, j), 0) >= 2:
                row += "m"
            elif hits.get((i, j), 0) == 1:
                row += "d"
            elif (i, j) in whole:
                row += "q"
            else:
                row += "_"
        cells.append(row)
    vals = [[tri[i][j] if j <= i else None for j in range(n)] for i in range(n)]
    return vz.grid(cells, values=vals)


rec.step(
    f"Find the maximum of the size-{K} triangle with its apex at row 0, column 0. It has "
    f"{K * (K + 1) // 2} cells. The last size built before {K} was {m}.",
    g=frame(0),
)
rec.step(
    f"Place three size-{m} triangles: one at the apex, and two at the bottom corners, each "
    f"{off} row{'s' if off > 1 else ''} down. Their apexes are (0, 0), ({off}, 0) and ({off}, {off}).",
    g=frame(0),
)
vals = []
for idx, (a, b) in enumerate(corners):
    v = tmax(a, b, m)
    vals.append(v)
    rec.step(
        f"The {names[idx]} triangle has its apex at ({a}, {b}) and covers {m * (m + 1) // 2} cell{'' if m == 1 else 's'}. "
        f"Its maximum is {v}.",
        g=frame(idx + 1),
    )
answer = max(vals)
hits = {}
for a, b in corners:
    for cell in tri_cells(a, b, m):
        hits[cell] = hits.get(cell, 0) + 1
shared = sum(1 for c in whole if hits.get(c, 0) >= 2)
if shared:
    tail = (f"{shared} cell{' is' if shared == 1 else 's are'} in two or more triangles and read "
            "more than once, which does not change a maximum.")
else:
    tail = "No cell is in two triangles: for size 2, the three cells are the three triangles."
rec.step(
    f"Every cell of the size-{K} triangle is in at least one of the three. The maximum is "
    f"max({', '.join(map(str, vals))}) = {answer}. {tail}",
    g=frame(3),
)

cur = {1: tri}
lv = tri
for a, b in zip(sizes, sizes[1:]):
    o = b - a
    lv = [[max(lv[i][j], lv[i + o][j], lv[i + o][j + o]) for j in range(i + 1)]
          for i in range(n - b + 1)]
rec.output("\n".join(" ".join(map(str, row)) for row in lv) + "\n")
