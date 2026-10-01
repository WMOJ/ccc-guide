import vizrec as vz

LIMIT = 10 ** 7
rec = vz.Recorder()
tokens = rec.stdin.split()
count = int(tokens[0])
pos = 1
powers = []
bounds = []
for _ in range(count):
    powers.append(int(tokens[pos]))
    pos += 1
    row = []
    for _ in range(3):
        row.append(int(tokens[pos]))
        pos += 1
    bounds.append(row)

names = {1: "N", 2: "N^2", 3: "N^3"}
marks = [["_"] * 3 for _ in range(count)]
lines = []


def frame():
    cells = []
    for i in range(count):
        cells.append([names[powers[i]]] + [str(b) for b in bounds[i]])
    states = ["_" + "".join(m) for m in marks]
    return vz.table(
        cells=cells,
        states=states,
        row_heads=[f"P{i + 1}" for i in range(count)],
        col_heads=["brute", "sub 1", "sub 2", "sub 3"],
    )


rec.step(
    f"{count} statements read. Each row gives the growth of that problem's brute force and the "
    f"bound on N in its three subtasks. Counting one operation per step, the budget here is "
    f"{LIMIT:,} operations. Nothing is marked yet.",
    table=frame(),
)
for i in range(count):
    reached = 0
    parts = []
    for j in range(3):
        ops = bounds[i][j] ** powers[i]
        if ops <= LIMIT:
            marks[i][j] = "d"
            reached += 1
            parts.append(f"{bounds[i][j]} gives {ops:,}, within budget")
        else:
            marks[i][j] = "x"
            parts.append(f"{bounds[i][j]} gives {ops:,}, over")
    text = f"P{i + 1} with {names[powers[i]]} growth: " + "; ".join(parts) + f". A brute force reaches {reached} of 3."
    lines.append(f"problem {i + 1}: brute force reaches {reached} of 3 subtasks")
    rec.step(text, table=frame())
rec.step(
    "The table is the start of your estimates: the subtasks marked within budget are the ones "
    "whose first attempt can be a brute force.",
    table=frame(),
)
rec.output("\n".join(lines) + "\n")
