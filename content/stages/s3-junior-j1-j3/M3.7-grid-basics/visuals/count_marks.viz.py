import vizrec as vz

rec = vz.Recorder()
r, c = map(int, rec.readline().split())
grid = [rec.readline() for _ in range(r)]

state = [["none"] * c for _ in range(r)]
count = 0


def frame():
    values = [[grid[row][col] for col in range(c)] for row in range(r)]
    return vz.grid(state, values=values)


rec.step(
    f"The scan starts at row 0, column 0 of a {r}-by-{c} board. No cell has been visited "
    "yet, and the count of marked cells is 0.",
    grid=frame(),
)
for row in range(r):
    for col in range(c):
        state[row][col] = "current"
        if grid[row][col] == "#":
            count += 1
            note = f"grid[{row}][{col}] is '#', so count becomes {count}."
        else:
            note = f"grid[{row}][{col}] is '.', so count stays {count}."
        rec.step(
            f"Row {row}, column {col} is current. {note}",
            grid=frame(),
        )
        state[row][col] = "done"

rec.step(
    f"Every cell has been visited in row-major order. The board holds {count} marked cells.",
    grid=frame(),
)
rec.output(f"{count}\n")
