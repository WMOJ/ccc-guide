import vizrec as vz

rec = vz.Recorder()
r, c = map(int, rec.readline().split())
grid = [list(map(int, rec.readline().split())) for _ in range(r)]

state = [["none"] * c for _ in range(r)]
row_sums = []
col_sums = []


def board():
    return vz.grid(state, values=grid)


def clear():
    for row in range(r):
        for col in range(c):
            state[row][col] = "none"


rec.step(
    f"A {r}-by-{c} grid of numbers. The program prints each row's sum first, then each column's "
    "sum. No sum is computed yet.",
    grid=board(),
    totals=vz.array(["?"] * r, name="row sums"),
)
for row in range(r):
    clear()
    for col in range(c):
        state[row][col] = "current"
    row_sums.append(sum(grid[row]))
    parts = " + ".join(str(v) for v in grid[row])
    rec.step(
        f"Row {row}: `sum(grid[{row}])` is {parts} = {row_sums[-1]}.",
        grid=board(),
        totals=vz.array(row_sums + ["?"] * (r - row - 1), states={row: "current"}, name="row sums"),
    )
for col in range(c):
    clear()
    for row in range(r):
        state[row][col] = "compare"
    col_sums.append(sum(grid[row][col] for row in range(r)))
    parts = " + ".join(str(grid[row][col]) for row in range(r))
    rec.step(
        f"Column {col}: the row index changes while `col` stays {col}, so the cells are "
        f"`grid[0][{col}]` down to `grid[{r - 1}][{col}]`. {parts} = {col_sums[-1]}.",
        grid=board(),
        totals=vz.array(col_sums + ["?"] * (c - col - 1), states={col: "compare"}, name="col sums"),
    )
clear()
rec.step(
    "Row sums: " + ", ".join(str(s) for s in row_sums) + ". Column sums: "
    + ", ".join(str(s) for s in col_sums) + f". {r} rows give {r} row sums, {c} columns give {c} column sums.",
    grid=board(),
    totals=vz.array(col_sums, name="col sums"),
)
rec.output("".join(f"{s}\n" for s in row_sums) + " ".join(str(s) for s in col_sums) + "\n")
