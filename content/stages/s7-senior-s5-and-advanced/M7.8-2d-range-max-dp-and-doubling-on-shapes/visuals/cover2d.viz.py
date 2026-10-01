import vizrec as vz

rec = vz.Recorder()
data = rec.stdin.split()
n = int(data[0])
grid = [[int(data[1 + i * n + j]) for j in range(n)] for i in range(n)]
pos = 1 + n * n
q = int(data[pos])
pos += 1
r, c, s = int(data[pos]), int(data[pos + 1]), int(data[pos + 2])

k = s.bit_length() - 1
size = 1 << k
far = s - size
corners = [(r, c), (r, c + far), (r + far, c), (r + far, c + far)]


def block_max(a, b):
    return max(grid[i][j] for i in range(a, a + size) for j in range(b, b + size))


def cells_of(a, b):
    return {(i, j) for i in range(a, a + size) for j in range(b, b + size)}


def frame(upto):
    hits = {}
    for a, b in corners[:upto]:
        for cell in cells_of(a, b):
            hits[cell] = hits.get(cell, 0) + 1
    states = []
    for i in range(n):
        row = ""
        for j in range(n):
            h = hits.get((i, j), 0)
            if h >= 2:
                row += "m"
            elif h == 1:
                row += "d"
            elif r <= i < r + s and c <= j < c + s:
                row += "q"
            else:
                row += "_"
        states.append(row)
    return vz.grid(states, values=grid)


rec.step(
    f"A query for the maximum of the square of side {s} whose top-left corner is row {r}, column {c}.",
    g=frame(0),
)
rec.step(
    f"The largest power of two that fits in {s} is 2^{k} = {size}, since ({s}).bit_length() - 1 = {k}. "
    f"Blocks of side {size} will cover the square.",
    g=frame(0),
)
names = ["top-left", "top-right", "bottom-left", "bottom-right"]
vals = []
for idx, (a, b) in enumerate(corners):
    m = block_max(a, b)
    vals.append(m)
    if far == 0:
        tail = " With side a power of two, this is the whole square, and the other three are the same block."
    else:
        tail = ""
    rec.step(
        f"The {names[idx]} block, table level {k} at ({a}, {b}), covers rows {a} to {a + size - 1} and "
        f"columns {b} to {b + size - 1}. Its maximum is {m}.{tail}",
        g=frame(idx + 1),
    )
    if far == 0:
        break
answer = max(vals)
if far == 0:
    text = f"One lookup gives the answer, {answer}. Four lookups would read the same cell four times."
else:
    text = (f"The answer is max({', '.join(map(str, vals))}) = {answer}. Cells shared by two or more "
            f"blocks were read more than once, which does not change a maximum.")
rec.step(text, g=frame(len(corners)))
rec.output(f"{answer}\n")
