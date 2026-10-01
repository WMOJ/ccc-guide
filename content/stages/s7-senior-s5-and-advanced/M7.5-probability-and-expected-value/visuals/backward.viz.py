import vizrec as vz

rec = vz.Recorder()
n, p_text = rec.readline().split()
n = int(n)
p = float(p_text)
q = 1 - p

e = [None] * (n + 2)
e[n] = 0.0
e[n + 1] = 0.0
heads = list(range(n + 2))


def fmt(x):
    return f"{x:g}"


def frame(filled_from, current=None, deps=()):
    cells = [[e[i] if e[i] is not None else "?" for i in range(n + 2)]]
    states = {}
    for i in range(n + 2):
        if e[i] is not None:
            states[(0, i)] = "done"
    for d in deps:
        states[(0, d)] = "compare"
    if current is not None:
        states[(0, current)] = "current"
    arrows = [((0, d), (0, current)) for d in deps] if current is not None else None
    return vz.table(cells, states=states, row_heads=["E"], col_heads=heads, row_title="", arrows=arrows)


rec.step(
    f"`e[i]` is the expected number of turns still to play from square `i`. Squares {n} and {n + 1} "
    "are past the end of the strip, so no turns are left there: both are 0. Every other cell is "
    "unknown (?), and each one will be computed from cells to its right.",
    t=frame(n),
)
for i in range(n - 1, -1, -1):
    a = e[i + 1]
    b = e[i + 2]
    value = 1 + p * a + q * b
    e[i] = value
    if i == n - 1:
        why = (
            f"One turn is always played. Then the token is on square {i + 1} or {i + 2}, past the end, "
            "with nothing left to play."
        )
    else:
        why = (
            f"One turn is played, then the token is on square {i + 1} or {i + 2}, and the cells "
            "for both are already filled."
        )
    rec.step(
        f"e[{i}] = 1 + {fmt(p)} * e[{i + 1}] + {fmt(q)} * e[{i + 2}] = 1 + {fmt(p)} * {fmt(a)} + "
        f"{fmt(q)} * {fmt(b)} = {fmt(value)}. {why}",
        t=frame(i, current=i, deps=(i + 1, i + 2)),
    )
rec.step(
    f"The table is full. e[0] = {fmt(e[0])} is the expected number of turns for the whole game, "
    "reached after computing each square once.",
    t=frame(0),
)
rec.output(str([e[i] for i in range(n)]) + "\n")
