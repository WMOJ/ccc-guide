import vizrec as vz

rec = vz.Recorder()
kg = int(rec.readline())
km = int(rec.readline())
cost = kg * 2 + km // 10

right = "Standard" if cost <= 20 else ("Priority" if cost <= 50 else "Express")
wrong = "Standard" if cost < 20 else ("Priority" if cost < 50 else "Express")
heads = ["right", "wrong"]


def table(k):
    cells = [["<= 20, <= 50", "?"], ["< 20, < 50", "?"]]
    states = {}
    if k >= 1:
        cells[0][1] = right
        states[(0, 1)] = "done"
    if k >= 2:
        cells[1][1] = wrong
        states[(1, 1)] = "done" if wrong == right else "invalid"
    if k < 2:
        states[(k, 0)] = "current"
    return vz.table(cells, states=states, row_heads=heads, col_heads=["checks", "prints"])


rec.step(
    f"The cost is {cost}. Two versions of the same chain differ only in the comparison: "
    "<= against <.",
    table=table(0),
)
rec.step(
    f"With <=, the first check is {cost} <= 20 and the second is {cost} <= 50. "
    f"The program prints {right}, which is what the problem asks.",
    table=table(1),
)
if wrong == right:
    rec.step(
        f"With <, the answer is also {wrong}. This cost sits away from a boundary, so the wrong "
        "comparison hides and this test would not catch it.",
        table=table(2),
    )
else:
    rec.step(
        f"With <, {cost} is not below the boundary, so it falls through to the next branch "
        f"and the program prints {wrong}. That is wrong, and only a test on the boundary shows it.",
        table=table(2),
    )
rec.output(f"{right}\n")
