import math

import vizrec as vz

rec = vz.Recorder()
a, b = map(int, rec.readline().split())

exact = a / b
fl = a // b
pr = a % b
tq = abs(a) // abs(b)
if (a < 0) != (b < 0):
    tq = -tq
tr = a - tq * b


def line(points):
    return vz.line(-5, 5, tick=1, points=points)


def tab(rows, states=None):
    return vz.table(rows, states=states, row_heads=["Python", "C++"], col_heads=["q", "r", "q*b + r"])


unknown = [["?", "?", "?"], ["?", "?", "?"]]
exact_pt = (exact, None, "compare")
rec.step(
    f"a is {a} and b is {b}. The exact quotient {a} / {b} is {exact}, which sits between "
    f"{math.floor(exact)} and {math.ceil(exact)} on the number line.",
    l=line([exact_pt]),
    t=tab(unknown),
)
rows = [[str(fl), str(pr), "?"], ["?", "?", "?"]]
rec.step(
    f"Python's `//` rounds down to {fl}, the whole number to the left. The remainder is "
    f"`a - q * b` = {a} - ({fl} * {b}) = {pr}, so `%` takes the sign of b.",
    l=line([exact_pt, (fl, "py", "current")]),
    t=tab(rows, {(0, 0): "current", (0, 1): "current"}),
)
rows = [[str(fl), str(pr), "?"], [str(tq), str(tr), "?"]]
if tq == fl:
    text = (
        f"C++ cuts the fraction off toward zero and lands on {tq} too: with a positive exact "
        f"quotient, rounding down and cutting toward zero are the same move. Its remainder is {tr}."
    )
else:
    text = (
        f"C++ cuts the fraction off toward zero and gets {tq}, not {fl}. Its remainder is "
        f"{a} - ({tq} * {b}) = {tr}, so C++ `%` takes the sign of a."
    )
rec.step(
    text,
    l=line([exact_pt, (fl, "py", "current"), (tq, "c++", "done")]) if tq != fl
    else line([exact_pt, (tq, "both", "done")]),
    t=tab(rows, {(1, 0): "done", (1, 1): "done"}),
)
rows = [[str(fl), str(pr), str(fl * b + pr)], [str(tq), str(tr), str(tq * b + tr)]]
rec.step(
    f"Each language keeps `q * b + r` equal to a: {fl * b} + ({pr}) = {a} for Python and "
    f"{tq * b} + ({tr}) = {a} for C++. The two only differ in which way q rounds.",
    l=line([exact_pt, (fl, "py", "current"), (tq, "c++", "done")]) if tq != fl
    else line([exact_pt, (tq, "both", "done")]),
    t=tab(rows, {(0, 2): "m", (1, 2): "m"}),
)
rec.output(f"python {fl} {pr}\nc++ {tq} {tr}\n")
