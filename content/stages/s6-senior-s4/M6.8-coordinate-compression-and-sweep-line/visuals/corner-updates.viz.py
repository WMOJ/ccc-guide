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
diff = [[0] * len(xs) for _ in range(len(ys))]
names = "ABC"



def table_frame(states=None, cells_only=False):
    if cells_only:
        rows = [row[:-1] for row in diff[:-1]]
        return vz.table(rows, states=states, row_heads=ys[:-1], col_heads=xs[:-1],
                        row_title="y", col_title="x")
    return vz.table(diff, states=states, row_heads=ys, col_heads=xs, row_title="y", col_title="x")


rec.step(
    f"The diff table has one row per y value and one column per x value, all zeros: "
    f"{len(ys)} by {len(xs)} for {n} rectangles. The headings are the original coordinates; the "
    "position of a heading is its rank.",
    diff=table_frame(),
)

for idx, (x1, y1, x2, y2) in enumerate(rects):
    left = x_rank[x1]
    right = x_rank[x2]
    top = y_rank[y1]
    bottom = y_rank[y2]
    diff[top][left] += 1
    diff[top][right] -= 1
    diff[bottom][left] -= 1
    diff[bottom][right] += 1
    marks = {(top, left): "compare", (top, right): "compare",
             (bottom, left): "compare", (bottom, right): "compare"}
    rec.step(
        f"Rectangle {names[idx]} has its corners at ranks (column {left}, row {top}) and "
        f"(column {right}, row {bottom}). Four entries change: +1 at its top-left, -1 at its "
        "top-right, -1 at its bottom-left and +1 at its bottom-right. No other entry is touched.",
        diff=table_frame(states=marks),
    )

rows = len(ys) - 1
cols = len(xs) - 1
rec.step(
    f"All {n} rectangles are recorded with {4 * n} small updates. The last row and column only "
    f"ever hold -1 and +1 marks, so the cells are the {rows} by {cols} block above and to the "
    "left. A running sum over that block, one row at a time, turns marks into depths.",
    diff=table_frame(cells_only=True),
)

for j in range(rows):
    for i in range(cols):
        if j > 0:
            diff[j][i] += diff[j - 1][i]
        if i > 0:
            diff[j][i] += diff[j][i - 1]
        if i > 0 and j > 0:
            diff[j][i] -= diff[j - 1][i - 1]
    states = ["d" * cols if r < j else ("c" * cols if r == j else "_" * cols) for r in range(rows)]
    if j == 0:
        how = "There is no row above, so each cell adds only the cell to its left."
    elif j >= 2:
        how = "Each cell follows the same rule as in row 1."
    else:
        how = ("Each cell adds the cell above and the cell to its left, then subtracts the cell "
               "above and to the left, which was added twice.")
    rec.step(
        f"Row {j} (y = {ys[j]}). {how} It now reads {diff[j][:cols]}.",
        diff=table_frame(states=states, cells_only=True),
    )

at_least_one = 0
at_least_two = 0
for j in range(rows):
    for i in range(cols):
        area = (xs[i + 1] - xs[i]) * (ys[j + 1] - ys[j])
        if diff[j][i] >= 1:
            at_least_one += area
        if diff[j][i] >= 2:
            at_least_two += area
rec.step(
    "Every cell now holds how many rectangles cover it. A cell holding 0 is uncovered; the "
    "areas come from multiplying by each cell's width and height, which the next figure does.",
    diff=table_frame(states=["d" * cols] * rows, cells_only=True),
)
rec.output(f"{at_least_one}\n{at_least_two}\n")
