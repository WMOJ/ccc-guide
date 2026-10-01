import vizrec as vz

rec = vz.Recorder()
n = int(rec.readline())


def frame(rows_done, latest):
    cells = []
    values = []
    count = 0
    for i in range(n):
        row_cells = ""
        row_values = []
        for j in range(n):
            if j <= i:
                row_cells += "#"
                row_values.append("-")
            elif i < rows_done:
                count += 1
                row_cells += "c" if i == latest else "d"
                row_values.append(count)
            else:
                row_cells += "."
                row_values.append("")
        cells.append(row_cells)
        values.append(row_values)
    return vz.grid(cells, values=values, indices=True)


count = 0
for i in range(n):
    runs = n - 1 - i
    before = count
    count += runs
    if runs == 0:
        caption = (
            f"i = {i}: the inner loop starts at j = {i + 1}, but range({i + 1}, {n}) is empty, "
            f"so no pair is counted. count stays {count}."
        )
    else:
        word = "time" if runs == 1 else "times"
        caption = (
            f"i = {i}: j runs from {i + 1} to {n - 1}, {runs} {word}, so count goes from "
            f"{before} to {count}. Each counted cell shows the running count."
        )
    rec.step(caption, grid=frame(i + 1, i))

rec.step(
    f"Every row is done: count is {count}, the number of cells above the diagonal, "
    f"{n} * {n - 1} / 2. That is what the program prints.",
    grid=frame(n, -1),
)
rec.output(f"{count}\n")
