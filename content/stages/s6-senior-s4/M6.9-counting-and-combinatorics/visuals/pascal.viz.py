import vizrec as vz

rec = vz.Recorder()
n = int(rec.readline())

rows = []
row = [1]
for _ in range(n + 1):
    rows.append(row)
    below = [1]
    for c in range(1, len(row)):
        below.append(row[c - 1] + row[c])
    below.append(1)
    row = below


def frame(upto, mid=None):
    cells = []
    states = {}
    for r in range(n + 1):
        cells.append([rows[r][c] if (r <= upto and c <= r) else None for c in range(n + 1)])
        for c in range(r + 1):
            if r < upto:
                states[(r, c)] = "done"
            elif r == upto:
                states[(r, c)] = "current"
    arrows = None
    if mid is not None:
        r, c = upto, mid
        states[(r - 1, c - 1)] = "compare"
        states[(r - 1, c)] = "compare"
        arrows = [((r - 1, c - 1), (r, c)), ((r - 1, c), (r, c))]
    return vz.table(cells, states=states, row_heads=list(range(n + 1)),
                    col_heads=list(range(n + 1)), row_title="n", col_title="r", arrows=arrows)


for r in range(n + 1):
    if r == 0:
        caption = "Row 0 is a single 1: there is one way to choose nothing from nothing."
        mid = None
    elif r == 1:
        caption = "Row 1 is 1 1: choose 0 of 1 item in one way, or choose that 1 item in one way."
        mid = None
    else:
        mid = r // 2
        a, b = rows[r - 1][mid - 1], rows[r - 1][mid]
        caption = (
            f"Row {r} starts and ends with 1. The marked cell C({r}, {mid}) is the sum of the two "
            f"cells above it: C({r - 1}, {mid - 1}) + C({r - 1}, {mid}) = {a} + {b} = {a + b}."
        )
    rec.step(caption, t=frame(r, mid))

rec.output("\n".join(" ".join(map(str, r)) for r in rows) + "\n")
