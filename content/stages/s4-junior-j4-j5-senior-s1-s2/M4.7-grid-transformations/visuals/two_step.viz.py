import vizrec as vz

rec = vz.Recorder()
data = rec.stdin.split()
rows = int(data[0])
cols = int(data[1])
grid = []
for i in range(rows):
    grid.append([int(x) for x in data[2 + i * cols:2 + (i + 1) * cols]])

transposed = [[grid[i][j] for i in range(rows)] for j in range(cols)]
result = [["?"] * rows for _ in range(cols)]
left_state = [["none"] * rows for _ in range(cols)]
right_state = [["none"] * rows for _ in range(cols)]


def frame():
    return {
        "mid": vz.grid(left_state, values=transposed),
        "out": vz.grid(right_state, values=result),
    }


rec.step(
    f"Step one is already done: transposing the {rows}-by-{cols} source gives this {cols}-by-{rows} "
    "grid on the left. Step two reverses each of its rows, filling the result on the right.",
    **frame(),
)
for i in range(cols):
    for j in range(rows):
        left_state[i][j] = "current"
    result[i] = transposed[i][::-1]
    for j in range(rows):
        right_state[i][j] = "current"
    shown = ", ".join(str(v) for v in transposed[i])
    back = ", ".join(str(v) for v in result[i])
    if rows == 1:
        note = "A row of one value reads the same backward."
    else:
        note = "It reads backward in the result."
    rec.step(
        f"Row {i} of the transposed grid is {shown}. {note} Result row {i} is {back}.",
        **frame(),
    )
    for j in range(rows):
        left_state[i][j] = "done"
        right_state[i][j] = "done"

rec.step(
    f"Every row is reversed. The result is the source rotated 90 degrees clockwise: the source's "
    f"top-left value {grid[0][0]} is now in the top-right corner, at row 0, column {rows - 1}.",
    **frame(),
)
rec.output("\n".join(" ".join(map(str, row)) for row in result) + "\n")
