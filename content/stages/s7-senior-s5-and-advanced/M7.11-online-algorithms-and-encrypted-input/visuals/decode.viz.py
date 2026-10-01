import vizrec as vz

rec = vz.Recorder()
n = int(rec.readline())
a = [int(x) for x in rec.readline().split()]
q = int(rec.readline())
lines = [tuple(int(t) for t in rec.readline().split()) for _ in range(q)]

cells = [[f"{k} {x} {y}", "?", "?", "?"] for k, x, y in lines]
states = [["_"] * 4 for _ in lines]
arrows = []
last = 0
source = None
results = []


def frame(arrows_now):
    return {
        "t": vz.table(
            [list(r) for r in cells],
            states=["".join(s) for s in states],
            col_heads=["raw", "last", "means", "answer"],
            row_heads=[str(i + 1) for i in range(q)],
            arrows=arrows_now,
        )
    }


rec.step(
    f"{q} lines arrive and only the raw text is known. Positions decode as `(raw + last) % {n}`, "
    "new values as `(raw + last) % 100`, and `last` is the latest range answer, 0 at the start. "
    "In `means`, `[1,4]` is a range sum and `a3=10` sets position 3.",
    **frame([])
)
for i, (kind, x, y) in enumerate(lines):
    states[i] = ["c"] * 4
    cells[i][1] = last
    if kind == 1:
        p = (x + last) % n
        v = (y + last) % 100
        old = a[p]
        a[p] = v
        cells[i][2] = f"a{p}={v}"
        cells[i][3] = "-"
        text = (
            f"Line {i + 1} is `{kind} {x} {y}`, an update. With `last` = {last}, the position is "
            f"({x} + {last}) % {n} = {p} and the value is ({y} + {last}) % 100 = {v}. "
            f"`a[{p}]` changes from {old} to {v}. An update has no answer, so `last` stays {last}."
        )
    else:
        first = (x + last) % n
        second = (y + last) % n
        swapped = first > second
        lo, hi = (second, first) if swapped else (first, second)
        ans = sum(a[lo:hi + 1])
        cells[i][2] = f"[{lo},{hi}]"
        cells[i][3] = ans
        add = " + ".join(str(v) for v in a[lo:hi + 1])
        swap = " The first number is larger than the second, so they swap." if swapped else ""
        text = (
            f"Line {i + 1} is `{kind} {x} {y}`, a range question. With `last` = {last}, the ends "
            f"are ({x} + {last}) % {n} = {first} and ({y} + {last}) % {n} = {second}.{swap} "
            f"Positions {lo} to {hi} sum to {add} = {ans}."
        )
    arrows_now = []
    if source is not None:
        arrows_now = [((source, 3), (i, 1))]
        text += f" The {last} in the `last` column came from line {source + 1}'s answer."
    rec.step(text, **frame(arrows_now))
    states[i] = ["d"] * 4
    if kind == 2:
        last = ans
        source = i
        results.append(ans)
final = ", ".join(str(r) for r in results)
rec.step(
    f"The answers are {final}. Every line needed the answer of a range question above it before "
    "its own numbers meant anything.",
    **frame([])
)
rec.output("\n".join(str(r) for r in results) + "\n")
