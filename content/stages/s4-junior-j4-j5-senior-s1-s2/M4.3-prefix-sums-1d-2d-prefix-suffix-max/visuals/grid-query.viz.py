import vizrec as vz

rec = vz.Recorder()
data = rec.stdin.split()
idx = 0
rows, cols = int(data[idx]), int(data[idx + 1])
idx += 2
grid = []
for _ in range(rows):
    grid.append([int(x) for x in data[idx:idx + cols]])
    idx += cols
q = int(data[idx])
idx += 1
r1, c1, r2, c2 = (int(v) for v in data[idx:idx + 4])

prefix = [[0] * (cols + 1) for _ in range(rows + 1)]
for r in range(rows):
    for c in range(cols):
        prefix[r + 1][c + 1] = grid[r][c] + prefix[r][c + 1] + prefix[r + 1][c] - prefix[r][c]

# net[r][c] counts how many times each gauge has been added minus subtracted so far.
net = [[0] * cols for _ in range(rows)]


def frame(target=False):
    states = []
    for r in range(rows):
        row_states = []
        for c in range(cols):
            if target:
                inside = r1 <= r <= r2 and c1 <= c <= c2
                row_states.append("current" if inside else "none")
            elif net[r][c] > 0:
                row_states.append("done")
            elif net[r][c] < 0:
                row_states.append("invalid")
            else:
                row_states.append("none")
        states.append(row_states)
    return vz.grid(states, values=grid)


def add(rr, cc, sign):
    for r in range(rr):
        for c in range(cc):
            net[r][c] += sign


expected = sum(grid[r][c] for r in range(r1, r2 + 1) for c in range(c1, c2 + 1))
rec.step(
    f"The query asks for the gauges from row {r1} to {r2} and column {c1} to {c2}, marked here. "
    "The four steps after this one reach that rectangle using only prefix entries.",
    g=frame(target=True),
)

running = prefix[r2 + 1][c2 + 1]
add(r2 + 1, c2 + 1, 1)
rec.step(
    f"Start with prefix[{r2 + 1}][{c2 + 1}] = {running}: every gauge from the top-left corner "
    f"through row {r2} and column {c2}, each counted once.",
    g=frame(),
)

above = prefix[r1][c2 + 1]
add(r1, c2 + 1, -1)
running -= above
if r1 == 0:
    why = f"Row {r1} is the top row, so there is no strip above the rectangle: prefix[0][{c2 + 1}] is 0."
else:
    why = f"Subtract prefix[{r1}][{c2 + 1}] = {above}, the strip above the rectangle."
rec.step(f"{why} Running total: {running}.", g=frame())

left = prefix[r2 + 1][c1]
add(r2 + 1, c1, -1)
running -= left
if c1 == 0:
    why = f"Column {c1} is the left edge, so there is no strip to the left: prefix[{r2 + 1}][0] is 0."
else:
    why = f"Subtract prefix[{r2 + 1}][{c1}] = {left}, the strip to the left of the rectangle."
rec.step(f"{why} Running total: {running}.", g=frame())

corner = prefix[r1][c1]
add(r1, c1, 1)
running += corner
if corner == 0:
    why = f"The corner above and to the left holds no gauges here, so adding prefix[{r1}][{c1}] = 0 changes nothing."
else:
    why = (
        f"The corner above and to the left was subtracted twice, once in each strip. Add "
        f"prefix[{r1}][{c1}] = {corner} back."
    )
rec.step(f"{why} Running total: {running}.", g=frame())

count = (r2 - r1 + 1) * (c2 - c1 + 1)
word = "gauge" if count == 1 else "gauges"
rec.step(
    f"Only the rectangle is left counted once: {prefix[r2 + 1][c2 + 1]} - {above} - {left} + "
    f"{corner} = {running} mm, the same as adding the rectangle's {count} {word} directly.",
    g=frame(),
)

rec.output(str(running) + "\n")
