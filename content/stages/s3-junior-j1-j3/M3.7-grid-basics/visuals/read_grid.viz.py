import vizrec as vz

rec = vz.Recorder()
tokens = rec.stdin.split()
r = int(tokens[0])
c = int(tokens[1])
rows = tokens[2:2 + r]
n = len(tokens)
marks = sum(row.count("#") for row in rows)

cells = [["none"] * c for _ in range(r)]
values = [[rows[row][col] for col in range(c)] for row in range(r)]
tok = ["none"] * n


def frame(**kw):
    return dict(
        tokens=vz.array(tokens, states=list(tok), indices=True, **kw),
        grid=vz.grid(cells, values=values),
    )


rec.step(
    f"`sys.stdin.read().split()` cuts the input at whitespace into {n} tokens: the two counts, "
    f"then one token per row. The grid on the right is what the row tokens will become.",
    **frame(),
)
tok[0] = "current"
rec.step(
    f"`r = int(data[0])` reads the first token, {r}. The board has {r} rows.",
    **frame(),
)
tok[0] = "done"
tok[1] = "current"
rec.step(
    f"`c = int(data[1])` reads the second token, {c}. Every row has {c} columns.",
    **frame(),
)
tok[1] = "done"
for i in range(2, 2 + r):
    tok[i] = "compare"
rec.step(
    f"`data[2:2 + r]` is `data[2:{2 + r}]`: exactly the {r} tokens after the counts. Each one is a whole row, "
    "because a row has no spaces inside it.",
    **frame(ranges=[(2, 1 + r, f"data[2:{2 + r}]")]),
)
for row in range(r):
    tok[2 + row] = "current"
    for col in range(c):
        cells[row][col] = "current"
    rec.step(
        f"`grid[{row}]` is `data[{2 + row}]`, the string `{rows[row]}`. Its {c} characters fill "
        f"row {row} of the grid.",
        **frame(),
    )
    tok[2 + row] = "done"
    for col in range(c):
        cells[row][col] = "done"
rec.step(
    f"The grid holds {r} rows of {c} characters. `grid[{r - 1}][{c - 1}]` is `'{rows[-1][-1]}'`, "
    f"the last cell of the last row. Scanning this grid, as count_marks.py does, finds {marks} marks.",
    **frame(),
)
rec.output(f"{marks}\n")
