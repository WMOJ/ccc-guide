import vizrec as vz

rec = vz.Recorder()
data = rec.stdin.split()
idx = 0
rows, cols = int(data[idx]), int(data[idx + 1])
idx += 2
grid = []
for _ in range(rows):
    grid.append([int(x) for x in data[idx:idx + cols]])
    idx += cols
q = int(data[idx])
idx += 1
queries = []
for _ in range(q):
    r1, c1, r2, c2 = (int(v) for v in data[idx:idx + 4])
    idx += 4
    queries.append((r1, c1, r2, c2))

prefix = [[None] * (cols + 1) for _ in range(rows + 1)]


def grid_frame(rect=None):
    states = []
    for r in range(rows):
        row_states = []
        for c in range(cols):
            if rect and rect[0] <= r <= rect[2] and rect[1] <= c <= rect[3]:
                row_states.append("compare")
            else:
                row_states.append("none")
        states.append(row_states)
    return vz.grid(states, values=grid)


def table_frame(cur=None, arrows=None, extra_states=None):
    states = {}
    for r in range(rows + 1):
        for c in range(cols + 1):
            if prefix[r][c] is not None:
                states[(r, c)] = "done"
    if extra_states:
        states.update(extra_states)
    if cur is not None:
        states[cur] = "current"
    return vz.table(
        prefix,
        states=states,
        row_heads=list(range(rows + 1)),
        col_heads=list(range(cols + 1)),
        row_title="r",
        col_title="c",
        arrows=arrows,
    )


for c in range(cols + 1):
    prefix[0][c] = 0
for r in range(rows + 1):
    prefix[r][0] = 0
rec.step(
    "Row 0 and column 0 hold 0: the rainfall total over zero rows, or zero columns, is always 0.",
    g=grid_frame(),
    t=table_frame(),
)

for r in range(rows):
    for c in range(cols):
        prefix[r + 1][c + 1] = (
            grid[r][c] + prefix[r][c + 1] + prefix[r + 1][c] - prefix[r][c]
        )
        rec.step(
            f"prefix[{r + 1}][{c + 1}] adds this gauge's {grid[r][c]} mm, the total above it, "
            f"and the total to its left, then removes the corner counted by both: "
            f"{grid[r][c]} + {prefix[r][c + 1]} + {prefix[r + 1][c]} - {prefix[r][c]} = "
            f"{prefix[r + 1][c + 1]}.",
            g=grid_frame(),
            t=table_frame(
                (r + 1, c + 1),
                arrows=[
                    ((r, c + 1), (r + 1, c + 1)),
                    ((r + 1, c), (r + 1, c + 1)),
                    ((r, c), (r + 1, c + 1)),
                ],
            ),
        )

rec.step(
    f"The table is complete. prefix[{rows}][{cols}], the bottom-right corner, is the total "
    f"rainfall over the whole grid: {prefix[rows][cols]} mm.",
    g=grid_frame(),
    t=table_frame(),
)

for r1, c1, r2, c2 in queries:
    corners = {
        (r2 + 1, c2 + 1): "current",
        (r1, c2 + 1): "compare",
        (r2 + 1, c1): "compare",
        (r1, c1): "compare",
    }
    total = prefix[r2 + 1][c2 + 1] - prefix[r1][c2 + 1] - prefix[r2 + 1][c1] + prefix[r1][c1]
    rec.step(
        f"The rectangle from row {r1} to {r2}, column {c1} to {c2}, highlighted on the gauge "
        f"grid: include the corner at ({r2 + 1}, {c2 + 1}), exclude the strip above at "
        f"({r1}, {c2 + 1}) and the strip to the left at ({r2 + 1}, {c1}), then add back the "
        f"corner at ({r1}, {c1}) removed by both. {prefix[r2 + 1][c2 + 1]} - "
        f"{prefix[r1][c2 + 1]} - {prefix[r2 + 1][c1]} + {prefix[r1][c1]} = {total} mm.",
        g=grid_frame((r1, c1, r2, c2)),
        t=table_frame(extra_states=corners),
    )

rec.output(
    "\n".join(
        str(prefix[r2 + 1][c2 + 1] - prefix[r1][c2 + 1] - prefix[r2 + 1][c1] + prefix[r1][c1])
        for r1, c1, r2, c2 in queries
    )
    + "\n"
)
