import vizrec as vz

rec = vz.Recorder()
data = rec.stdin.split()
pos = 0
rows = int(data[pos])
cols = int(data[pos + 1])
pos += 2
grid = []
for _ in range(rows):
    grid.append(data[pos:pos + cols])
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
    f"columns, every cell still marked ?, because a transpose swaps rows for columns, so the shape swaps too.",
    **frame(),
)
for r in range(rows):
    for c in range(cols):
        source_state[r][c] = "current"
        target[c][r] = grid[r][c]
        target_state[c][r] = "current"
        rec.step(
            f"old[{r}][{c}] = '{grid[r][c]}' moves to new[{c}][{r}]: row {r} becomes column "
            f"{r}, and column {c} becomes row {c}.",
            **frame(),
        )
        source_state[r][c] = "done"
        target_state[c][r] = "done"

rec.step(
    "Every source cell has moved. The target is the source with rows and columns swapped.",
    **frame(),
)
rec.output("\n".join(" ".join(row) for row in target) + "\n")
