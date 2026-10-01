import vizrec as vz

rec = vz.Recorder()
k = int(rec.readline())
bounds = [int(t) for t in rec.readline().split()][:k]

BUDGET = 10**7


def counts(n):
    """Additions done by each plan on n values, checked against real loops below."""
    return n * (n + 1) * (n + 2) // 6, n * (n + 1) // 2, n


def counted(n):
    cubic = quadratic = 0
    for i in range(n):
        for j in range(i, n):
            quadratic += 1
            for _ in range(i, j + 1):
                cubic += 1
    return cubic, quadratic, n


for probe in range(1, 40):
    assert counts(probe) == counted(probe)


def sci(v):
    if v < 100000:
        return f"{v:,}"
    e = len(str(v)) - 1
    return f"{v / 10 ** e:.1f}e{e}"


def bound_text(n):
    if n >= 100000 and set(str(n)[1:]) == {"0"} and str(n)[0] == "1":
        return f"10^{len(str(n)) - 1}"
    return str(n)


PLANS = ["slice sums", "running sums", "prefix and minimum"]
rows = []
states = []
output = ""


def frame():
    return vz.table(
        cells=[list(r) for r in rows],
        states=list(states),
        row_heads=[f"N ≤ {bound_text(b)}" for b in bounds[: len(rows)]],
        col_heads=["O(N^3)", "O(N^2)", "O(N)"],
    )


def verdict(v):
    if v <= BUDGET:
        return "within the budget"
    return f"about {sci(v // BUDGET)} times the budget"


for s, n in enumerate(bounds, start=1):
    c = counts(n)
    rows.append([sci(v) for v in c])
    states.append("".join("d" if v <= BUDGET else "x" for v in c))
    text = (
        f"Subtask {s} bounds N at {bound_text(n)}. Slice sums do {sci(c[0])} additions, "
        f"{verdict(c[0])}. Running sums do {sci(c[1])}, {verdict(c[1])}. The prefix plan does "
        f"{sci(c[2])}, {verdict(c[2])}."
    )
    rec.step(text, table=frame())
    output += f"n={n} cubic={c[0]} quadratic={c[1]} linear={c[2]}\n"

rec.step(
    "Each bound rules out the plan that served the row above. In the last row only the prefix plan "
    "is within the budget.",
    table=frame(),
)
rec.output(output)
