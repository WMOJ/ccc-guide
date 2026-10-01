import vizrec as vz

rec = vz.Recorder()
rows, cols = map(int, rec.readline().split())
grid = []
for _ in range(rows):
    grid.append(list(map(int, rec.readline().split())))
cells = []
for row in grid:
    cells.extend(row)
r, c = map(int, rec.readline().split())
here = r * cols + c


def frames(gs=None, a_states=None, ptr=None):
    g_rows = []
    for i in range(rows):
        g_rows.append("".join(vz.code((gs or {}).get((i, j))) for j in range(cols)))
    return {
        "g": vz.grid(g_rows, values=grid),
        "a": vz.array(cells, states=a_states, pointers=ptr, indices=True),
    }


rec.step(
    f"The grid has {rows} rows and {cols} columns. `cells` holds the same {rows * cols} values, "
    f"row after row, so cell (r, c) sits at index `r * {cols} + c`.",
    **frames(),
)
rec.step(
    f"Cell ({r}, {c}) is at index {r} * {cols} + {c} = {here}, and `cells[{here}]` is {cells[here]}.",
    **frames({(r, c): "current"}, {here: "current"}, {"here": here}),
)

right = "none"
if c + 1 < cols:
    right = str(cells[here + 1])
    rec.step(
        f"Column {c} + 1 is {c + 1}, less than {cols}, so a right neighbor exists. It is the next index, "
        f"{here} + 1 = {here + 1}: `cells[{here + 1}]` is {right}.",
        **frames({(r, c): "current", (r, c + 1): "compare"}, {here: "current", here + 1: "compare"}, {"here": here}),
    )
else:
    wrong = here + 1
    gs = {(r, c): "current"}
    if wrong < rows * cols:
        gs[(wrong // cols, wrong % cols)] = "invalid"
        note = (
            f"Index {here} + 1 is {wrong}, which is cell ({wrong // cols}, {wrong % cols}) on the next row, "
            f"so the check `c + 1 < cols` fails first: column {c} + 1 is {c + 1}, not less than {cols}. No right neighbor."
        )
        states = {here: "current", wrong: "invalid"}
    else:
        note = (
            f"Column {c} + 1 is {c + 1}, not less than {cols}, so there is no right neighbor. "
            f"Index {here} + 1 is {wrong}, past the end of the list."
        )
        states = {here: "current"}
    rec.step(note, **frames(gs, states, {"here": here}))

down = "none"
if r + 1 < rows:
    down = str(cells[here + cols])
    rec.step(
        f"Row {r} + 1 is {r + 1}, less than {rows}. A row is {cols} cells long, so the cell below is "
        f"{cols} indexes on: {here} + {cols} = {here + cols}, and `cells[{here + cols}]` is {down}.",
        **frames({(r, c): "current", (r + 1, c): "compare"}, {here: "current", here + cols: "compare"}, {"here": here}),
    )
else:
    rec.step(
        f"Row {r} + 1 is {r + 1}, not less than {rows}, so there is no cell below. "
        f"Index {here} + {cols} would be {here + cols}, past the end of the list.",
        **frames({(r, c): "current"}, {here: "current"}, {"here": here}),
    )

rec.step(
    f"The program prints `cell {cells[here]} right {right} down {down}`.",
    **frames({(r, c): "current"}, {here: "current"}, {"here": here}),
)
rec.output(f"cell {cells[here]} right {right} down {down}\n")
