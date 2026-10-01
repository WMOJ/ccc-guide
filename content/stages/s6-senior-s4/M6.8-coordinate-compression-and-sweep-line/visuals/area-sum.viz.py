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
cols = len(xs) - 1
rows = len(ys) - 1
depth = [[0] * cols for _ in range(rows)]
for x1, y1, x2, y2 in rects:
    for j in range(y_rank[y1], y_rank[y2]):
        for i in range(x_rank[x1], x_rank[x2]):
            depth[j][i] += 1
widths = [xs[i + 1] - xs[i] for i in range(cols)]
heights = [ys[j + 1] - ys[j] for j in range(rows)]
size = max(rows, cols)


def grid_frame(current=None, finished=0, final=False):
    states = []
    for j in range(rows):
        row = ""
        for i in range(cols):
            if final and depth[j][i] >= 2:
                row += "m"
            elif j == current:
                row += "c"
            elif j < finished:
                row += "d"
            else:
                row += "_"
        states.append(row)
    return vz.grid(states, values=depth)


def sizes_frame(current=None):
    states = None
    if current is not None:
        states = {(1, current): "current"}
        for i in range(cols):
            states[(0, i)] = "current"
    return vz.table(
        [widths + [None] * (size - cols), heights + [None] * (size - rows)],
        states=states,
        row_heads=["width", "height"],
        col_heads=list(range(size)),
        col_title="column / row",
    )


rec.step(
    f"The depths from the last figure sit on the {rows} by {cols} grid. The table gives each "
    "column's original width and each row's original height. The area of a cell is its width times its "
    "row's height, and two totals start at 0: area covered by at least 1 rectangle, and by at least 2.",
    depth=grid_frame(),
    sizes=sizes_frame(),
)

total_one = 0
total_two = 0
for j in range(rows):
    one = 0
    two = 0
    areas = []
    for i in range(cols):
        area = widths[i] * heights[j]
        areas.append(area)
        if depth[j][i] >= 1:
            one += area
        if depth[j][i] >= 2:
            two += area
    total_one += one
    total_two += two
    rec.step(
        f"Row {j} has height {heights[j]}, so its cell areas are {areas} and its depths are "
        f"{depth[j]}. Depth 1 or more adds {one}, depth 2 or more adds {two}. The totals are "
        f"now {total_one} and {total_two}.",
        depth=grid_frame(current=j, finished=j),
        sizes=sizes_frame(current=j),
    )

tail = (
    "those cells are the ones marked Depth 2 or more."
    if total_two > 0
    else "no cell has depth 2, so no cell is marked."
)
rec.step(
    f"All rows are summed. The area covered by at least one rectangle is {total_one}. The area "
    f"covered by at least two is {total_two}; {tail}",
    depth=grid_frame(finished=rows, final=True),
    sizes=sizes_frame(),
)
rec.output(f"{total_one}\n{total_two}\n")
