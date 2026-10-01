import vizrec as vz

rec = vz.Recorder()
n, p_text = rec.readline().split()
n = int(n)
p = float(p_text)
q = 1 - p


def fmt(x):
    return f"{x:g}"


land = [None] * n
land[0] = 1.0


def frame(current=None, sources=(), sum_range=False):
    vals = [fmt(x) if x is not None else "?" for x in land]
    states = {}
    for i in range(n):
        if land[i] is not None:
            states[i] = "done"
    for s in sources:
        states[s] = "compare"
    if current is not None:
        states[current] = "current"
    ranges = [(1, n - 1, "add these, plus 1")] if sum_range and n > 1 else None
    return vz.array(vals, states=states, ranges=ranges)


rec.step(
    "Every turn ends on some square. The token starts on square 0, so `land[0]` is 1. "
    "`land[i]` will hold the chance that the token lands on square `i` at some point.",
    a=frame(current=0),
)
for i in range(1, n):
    if i == 1:
        value = p * land[0]
        text = (
            f"The token reaches square 1 only by a 1-step from square 0: land[1] = {fmt(p)} * "
            f"{fmt(land[0])} = {fmt(value)}."
        )
        sources = (0,)
    else:
        value = p * land[i - 1] + q * land[i - 2]
        text = (
            f"Square {i} is reached by a 1-step from square {i - 1} or a 2-step from square {i - 2}: "
            f"land[{i}] = {fmt(p)} * {fmt(land[i - 1])} + {fmt(q)} * {fmt(land[i - 2])} = {fmt(value)}."
        )
        sources = (i - 1, i - 2)
    land[i] = value
    rec.step(text, a=frame(current=i, sources=sources))
total = 1 + sum(land[1:])
if n == 1:
    tail = "There are no squares between the start and the end, so the only turn is the last one."
else:
    tail = (
        f"Each landing on squares 1 to {n - 1} is one turn, and the last turn lands on or past square "
        "{}. Adding the chances gives the expected turns, by linearity.".format(n)
    )
rec.step(
    f"{tail} Expected turns = 1 + {' + '.join(fmt(x) for x in land[1:]) or '0'} = {fmt(total)}.",
    a=frame(sum_range=True),
)
rec.output(f"{[land[i] for i in range(n)]}\nexpected turns: {total:.4f}\n")
