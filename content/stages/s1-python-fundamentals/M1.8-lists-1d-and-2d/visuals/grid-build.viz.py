import vizrec as vz

rec = vz.Recorder()
rows = int(rec.readline())
cols = int(rec.readline())

# The real lists, built both ways, so the printed results are the real ones.
shared = [[0] * cols] * rows
shared[0][1] = 5
separate = [[0] * cols for _ in range(rows)]
separate[0][1] = 5


def outer(names):
    return vz.array(names, states="m" * len(names) if len(set(names)) == 1 and rows > 1 else "d" * len(names), indices=True)


def row_table(row_lists, changed):
    states = []
    for r, row in enumerate(row_lists):
        states.append("".join("c" if (r == 0 and c == 1 and changed) else "d" for c in range(cols)))
    return vz.table(row_lists, states=states, row_heads=[f"row {i + 1}" for i in range(len(row_lists))], col_heads=list(range(cols)))


zeros = [[0] * cols]

if rows > 1:
    rec.step(
        f"`[[0] * {cols}] * {rows}` builds one row list, row 1, holding {cols} zeros. `* {rows}` does not copy it: "
        f"all {rows} entries of `grid` point at row 1.",
        a=outer(["row 1"] * rows),
        b=row_table(zeros, False),
    )
    rec.step(
        f"`grid[0][1] = 5` changes row 1. Every entry points at row 1, so all {rows} rows show the 5. "
        f"`print(grid)` shows {shared}.",
        a=outer(["row 1"] * rows),
        b=row_table([[0, 5] + [0] * (cols - 2)], True),
    )
else:
    rec.step(
        f"`[[0] * {cols}] * 1` builds one row list, row 1, and `* 1` keeps just that one entry. "
        "With a single entry, there is nothing for a second row to share.",
        a=outer(["row 1"]),
        b=row_table(zeros, False),
    )
    rec.step(
        f"`grid[0][1] = 5` changes row 1, the only row. `print(grid)` shows {shared}.",
        a=outer(["row 1"]),
        b=row_table([[0, 5] + [0] * (cols - 2)], True),
    )

names = [f"row {i + 1}" for i in range(rows)]
if rows > 1:
    build = f"`[[0] * {cols} for _ in range({rows})]` runs `[0] * {cols}` once per row, so the {rows} entries of `grid` hold {rows} different row lists."
else:
    build = f"`[[0] * {cols} for _ in range(1)]` also builds one row list, row 1, for the single entry of `grid`."
rec.step(
    build,
    a=outer(names),
    b=row_table([[0] * cols for _ in range(rows)], False),
)

fixed_tail = (
    "The other rows keep their zeros." if rows > 1 else "With one row, both ways give the same grid."
)
rec.step(
    f"`grid[0][1] = 5` changes only row 1. {fixed_tail} `print(grid)` shows {separate}.",
    a=outer(names),
    b=row_table(separate, True),
)

rec.output(f"{shared}\n")
