import vizrec as vz

rec = vz.Recorder()
data = rec.stdin.split()
pos = 0
rows = int(data[pos])
cols = int(data[pos + 1])
pos += 2
grid = []
for _ in range(rows):
    grid.append([int(x) for x in data[pos:pos + cols]])
    pos += cols

target = [["?"] * rows for _ in range(cols)]
source_state = [["none"] * cols for _ in range(rows)]
target_state = [["none"] * rows for _ in range(cols)]


def frame():
    return {
        "source": vz.grid(source_state, values=grid),
        "target": vz.grid(target_state, values=target),
    }


rec.step(
    f"The source is {rows} rows by {cols} columns. The target has {cols} rows by {rows} "
    f"columns, every cell still marked ?, because rotating 90 degrees swaps the dimensions.",
    **frame(),
)
for r in range(rows):
    for c in range(cols):
        source_state[r][c] = "current"
        nr, nc = c, rows - 1 - r
        target[nr][nc] = grid[r][c]
        target_state[nr][nc] = "current"
        rec.step(
            f"old[{r}][{c}] = {grid[r][c]} moves to new[{nr}][{nc}]: a clockwise turn sends "
            f"row {r} to column {rows - 1 - r}, and column {c} to row {c}.",
            **frame(),
        )
        source_state[r][c] = "done"
        target_state[nr][nc] = "done"

rec.step(
    "Every source cell has moved. The target is the source rotated 90 degrees clockwise.",
    **frame(),
)
rec.output("\n".join(" ".join(map(str, row)) for row in target) + "\n")
