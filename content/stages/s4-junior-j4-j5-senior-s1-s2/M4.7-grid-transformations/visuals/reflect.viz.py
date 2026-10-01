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

source_state = [["none"] * cols for _ in range(rows)]
result = [["?"] * cols for _ in range(rows)]
result_state = [["none"] * cols for _ in range(rows)]


def frame():
    return {
        "source": vz.grid(source_state, values=grid),
        "result": vz.grid(result_state, values=result),
    }


rec.step(
    f"The source is {rows} rows by {cols} columns. Reflecting horizontally reverses each row "
    "left to right; the shape stays the same.",
    **frame(),
)
for r in range(rows):
    for c in range(cols):
        source_state[r][c] = "current"
        nc = cols - 1 - c
        result[r][nc] = grid[r][c]
        result_state[r][nc] = "current"
        rec.step(
            f"old[{r}][{c}] = '{grid[r][c]}' moves to new[{r}][{nc}]: row {r} reverses "
            "left to right.",
            **frame(),
        )
        source_state[r][c] = "done"
        result_state[r][nc] = "done"
rec.step(
    "The horizontal reflection is done. Every row now reads backward.",
    **frame(),
)

for r in range(rows):
    for c in range(cols):
        source_state[r][c] = "none"
        result_state[r][c] = "none"
        result[r][c] = "?"

rec.step(
    "Now reflect the same source vertically: reverse the order of the rows top to bottom, "
    "leaving each row's own contents unchanged.",
    **frame(),
)
for r in range(rows):
    for c in range(cols):
        source_state[r][c] = "current"
        nr = rows - 1 - r
        result[nr][c] = grid[r][c]
        result_state[nr][c] = "current"
        rec.step(
            f"old[{r}][{c}] = '{grid[r][c]}' moves to new[{nr}][{c}]: row {r} becomes row "
            f"{nr}.",
            **frame(),
        )
        source_state[r][c] = "done"
        result_state[nr][c] = "done"
rec.step(
    "The vertical reflection is done. The rows are in reverse order; each row's own "
    "contents did not change.",
    **frame(),
)

h_result = [row[::-1] for row in grid]
v_result = grid[::-1]
out_lines = ["Original:"]
out_lines += [" ".join(row) for row in grid]
out_lines.append("")
out_lines.append("Horizontal reflection:")
out_lines += [" ".join(row) for row in h_result]
out_lines.append("")
out_lines.append("Vertical reflection:")
out_lines += [" ".join(row) for row in v_result]
rec.output("\n".join(out_lines) + "\n")
