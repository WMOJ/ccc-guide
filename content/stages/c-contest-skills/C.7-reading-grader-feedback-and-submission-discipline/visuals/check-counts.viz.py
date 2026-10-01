import vizrec as vz

rec = vz.Recorder()
mode = rec.readline().strip()
sizes = list(map(int, rec.readline().split()))
BUDGET = 10 ** 8


def slow_checks(values):
    checks = 0
    for i in range(len(values)):
        for j in range(i):
            checks += 1
            if values[j] == values[i]:
                return checks
    return checks


def fast_checks(values):
    seen = set()
    checks = 0
    for v in values:
        checks += 1
        if v in seen:
            return checks
        seen.add(v)
    return checks


def fmt(x):
    return f"{x:,}"


rows = []
states = []
output = ""


def frame():
    return vz.table(
        cells=[r[1:3] for r in rows],
        states=list(states),
        row_heads=[r[0] for r in rows],
        col_heads=["list scan", "set"],
        row_title="n",
    )


for n in sizes:
    values = list(range(n))
    if mode == "front":
        values[1] = values[0]
    slow = slow_checks(values)
    fast = fast_checks(values)
    output += f"{n} {slow} {fast}\n"
    over = slow > BUDGET
    rows.append((fmt(n), fmt(slow), fmt(fast), "yes" if over else "no"))
    states.append("xd" if over else "dd")
    if mode == "front":
        if n == sizes[0]:
            caption = (
                f"n = {fmt(n)}: two equal values sit at the front. The list scan finds the repeat "
                f"after {fmt(slow)} check and the set after {fmt(fast)}."
            )
        else:
            caption = (
                f"n = {fmt(n)}: still {fmt(slow)} check for the list scan and {fmt(fast)} for the "
                f"set, because the repeat is still at the front."
            )
    elif over:
        caption = (
            f"n = {fmt(n)}: the list scan makes {fmt(slow)} checks, past 10^8, while the set "
            f"still makes {fmt(fast)}, one per value."
        )
    else:
        caption = (
            f"n = {fmt(n)}: the list scan makes {fmt(slow)} checks and the set makes {fmt(fast)}. "
            f"Both are under 10^8."
        )
    rec.step(caption, table=frame())

if mode == "front":
    rec.step(
        "With a repeat at the front, the quadratic version finishes at once at every n. "
        "A test like this never shows the slowness of the list scan.",
        table=frame(),
    )
else:
    rec.step(
        "With no repeat, the list scan checks every pair: about 100 times more checks for each "
        "tenfold n. The set makes one lookup per value.",
        table=frame(),
    )
rec.output(output)
