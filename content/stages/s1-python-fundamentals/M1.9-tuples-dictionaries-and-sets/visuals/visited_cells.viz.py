"""StepThrough: visited_cells.py, a set of (row, col) tuples beside the grid they describe.

Two panels: `grid` (3 by 3) and `visited` (StructViz set of tuples). Consistency: rec.output()
must equal visited_cells.py's real stdout for the same stdin.
"""

import vizrec as vz

rec = vz.Recorder()

SIZE = 3


def grid_frame(visited, current=None, repeat=False):
    rows = []
    values = []
    for r in range(SIZE):
        states = ""
        vals = []
        for c in range(SIZE):
            if (r, c) == current:
                states += "x" if repeat else "c"
            elif (r, c) in visited:
                states += "d"
            else:
                states += "."
            vals.append("v" if (r, c) in visited else "-")
        rows.append(states)
        values.append(vals)
    return vz.grid(rows, values=values)


def set_frame(order, current=None, repeat=False):
    items = []
    for cell in order:
        s = None
        if cell == current:
            s = "x" if repeat else "c"
        items.append({"v": f"({cell[0]}, {cell[1]})", "s": s})
    return vz.struct("set", items)


n = int(rec.readline())
order = []
visited = set()
out = ""
for _ in range(n):
    row, col = map(int, rec.readline().split())
    cell = (row, col)
    if cell in visited:
        rec.step(
            f"The pair ({row}, {col}) is already in `visited`, so `(row, col) in visited` is True. "
            f'The program prints "again {row} {col}" and adds nothing.',
            grid=grid_frame(visited, current=cell, repeat=True),
            visited=set_frame(order, current=cell, repeat=True),
        )
        out += f"again {row} {col}\n"
    else:
        visited.add(cell)
        order.append(cell)
        rec.step(
            f"`({row}, {col}) in visited` is False, so `visited.add(({row}, {col}))` stores the whole "
            f"pair as one value. The grid marks row {row}, column {col}.",
            grid=grid_frame(visited, current=cell),
            visited=set_frame(order, current=cell),
        )

rec.step(
    f"`len(visited)` is {len(visited)}, the number of different cells stored, however many lines "
    "named them.",
    grid=grid_frame(visited),
    visited=set_frame(order),
)
out += f"{len(visited)}\n"

rec.output(out)
rec.done()
