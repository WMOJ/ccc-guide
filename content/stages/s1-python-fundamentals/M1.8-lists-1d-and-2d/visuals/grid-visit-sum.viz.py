import vizrec as vz

rec = vz.Recorder()
rows = int(rec.readline())
cols = int(rec.readline())
grid = [list(map(int, rec.readline().split())) for _ in range(rows)]

states = [["."] * cols for _ in range(rows)]


def frame():
    return vz.grid([[states[r][c] for c in range(cols)] for r in range(rows)], values=grid, indices=True)


rec.step(f"Start with a {rows}-by-{cols} grid. total is 0.", g=frame())

total = 0
for r in range(rows):
    for c in range(cols):
        value = grid[r][c]
        total += value
        states[r][c] = "current"
        rec.step(
            f"grid[{r}][{c}] is {value}, so total becomes {total}.",
            g=frame(),
        )
        states[r][c] = "done"

rec.step(f"Every cell is visited. total is {total}.", g=frame())
rec.output(f"{total}\n")
