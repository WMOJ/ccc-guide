import vizrec as vz

rec = vz.Recorder()
data = rec.stdin.split()
n = int(data[0])
pos = 1
rects = []
xs = set()
ys = set()
for _ in range(n):
    x1 = int(data[pos])
    y1 = int(data[pos + 1])
    x2 = int(data[pos + 2])
    y2 = int(data[pos + 3])
    pos += 4
    rects.append((x1, y1, x2, y2))
    xs.add(x1)
    xs.add(x2)
    ys.add(y1)
    ys.add(y2)
xs = sorted(xs)
ys = sorted(ys)
x_rank = {x: i for i, x in enumerate(xs)}
y_rank = {y: i for i, y in enumerate(ys)}
widths = [xs[i + 1] - xs[i] for i in range(len(xs) - 1)]
heights = [ys[j + 1] - ys[j] for j in range(len(ys) - 1)]
cols = len(widths)
rows = len(heights)
depth = [[0] * cols for _ in range(rows)]
names = "ABC"


def span(word, a, b):
    if a == b:
        return f"{word} {a}"
    return f"{word}s {a} to {b}"


def grid_frame(active=None):
    states = []
    for j in range(rows):
        row = ""
        for i in range(cols):
            if active is not None and active[0] <= i < active[1] and active[2] <= j < active[3]:
                row += "c"
            elif depth[j][i] > 0:
                row += "d"
            else:
                row += "_"
        states.append(row)
    return vz.grid(states, values=depth)


def sizes_frame():
    size = max(rows, cols)
    return vz.table(
        [widths + [None] * (size - cols), heights + [None] * (size - rows)],
        row_heads=["width", "height"],
        col_heads=list(range(size)),
        col_title="column / row",
    )


rec.step(
    f"{n} rectangles have {len(xs)} distinct x values and {len(ys)} distinct y values, so the "
    f"compressed grid has {cols} columns and {rows} rows. No cell is covered yet. Each column and "
    "row keeps the original distance between its two boundary coordinates.",
    grid=grid_frame(),
    sizes=sizes_frame(),
)

lines = []
for idx, (x1, y1, x2, y2) in enumerate(rects):
    left = x_rank[x1]
    right = x_rank[x2]
    top = y_rank[y1]
    bottom = y_rank[y2]
    count = (right - left) * (bottom - top)
    rec.step(
        f"Rectangle {names[idx]} has corner ranks {span('column', left, right)} and "
        f"{span('row', top, bottom)}. It covers the cells in {span('column', left, right - 1)} and "
        f"{span('row', top, bottom - 1)}: {count} cell{'' if count == 1 else 's'}.",
        grid=grid_frame(active=(left, right, top, bottom)),
        sizes=sizes_frame(),
    )
    for j in range(top, bottom):
        for i in range(left, right):
            depth[j][i] += 1
    lines.append(f"columns {left} to {right} rows {top} to {bottom}")
    rec.step(
        f"Rectangle {names[idx]} is painted: every cell it covers went up by 1. Painting cell by "
        "cell costs one step for each cell of the rectangle.",
        grid=grid_frame(),
        sizes=sizes_frame(),
    )

top_depth = max(max(row) for row in depth)
rec.step(
    f"All {n} rectangles are painted. The largest depth is {top_depth}; a cell with a 0 is not "
    "covered by any rectangle.",
    grid=grid_frame(),
    sizes=sizes_frame(),
)
rec.output(
    "widths %s\nheights %s\n" % (widths, heights) + "".join("columns %d to %d rows %d to %d\n" % (
        x_rank[x1], x_rank[x2], y_rank[y1], y_rank[y2]) for x1, y1, x2, y2 in rects)
)
