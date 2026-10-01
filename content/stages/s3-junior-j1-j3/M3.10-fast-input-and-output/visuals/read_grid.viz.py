import vizrec as vz

rec = vz.Recorder()
tokens = rec.stdin.split()
rows = int(tokens[0])
cols = int(tokens[1])
values = [int(t) for t in tokens[2 : 2 + rows * cols]]

grid = [[None] * cols for _ in range(rows)]
states = [["none"] * cols for _ in range(rows)]

k = 0
total = 0
for r in range(rows):
    for c in range(cols):
        val = values[k]
        grid[r][c] = val
        states[r][c] = "current"
        total += val
        rec.step(
            f"rows = {rows}, cols = {cols}. Token {k + 2} is {val}, placed at grid[{r}][{c}].",
            grid=vz.table(grid, states=states, row_title="row", col_title="col"),
        )
        states[r][c] = "done"
        k += 1

cell_count = rows * cols
rec.step(
    f"All {cell_count} value{'s' if cell_count != 1 else ''} placed. Summing every cell gives {total}.",
    grid=vz.table(grid, states=[["done"] * cols for _ in range(rows)], row_title="row", col_title="col"),
)

rec.output(f"{total}\n")
