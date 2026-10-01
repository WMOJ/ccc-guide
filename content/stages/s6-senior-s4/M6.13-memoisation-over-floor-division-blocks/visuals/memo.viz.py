import vizrec as vz

rec = vz.Recorder()
n = int(rec.readline())

values = []
d = 1
while d <= n:
    q = n // d
    values.append(q)
    d = n // q + 1
values.reverse()

cost = {}


def table(current=None):
    top = [str(v) for v in values]
    bottom = [cost[v] if v in cost else "?" for v in values]
    states = {}
    for c, v in enumerate(values):
        if v in cost:
            states[(1, c)] = "done"
    if current is not None:
        states[(1, values.index(current))] = "current"
        states[(0, values.index(current))] = "current"
    return vz.table([top, bottom], states=states or None, row_heads=["value v", "cost(v)"])


rec.step(
    f"`{n} // d` takes only {len(values)} different value{'s' if len(values) != 1 else ''}, "
    "listed here smallest first. The memo table will hold cost(v) for each, using the rule "
    "that cost(v) is v plus the sum of cost(v // d) for d = 2 to v.",
    t=table()
)
for v in values:
    total = v
    parts = []
    d = 2
    while d <= v:
        q = v // d
        last = v // q
        total += cost[q] * (last - d + 1)
        size = last - d + 1
        parts.append(f"{size} * cost({q})" if size > 1 else f"cost({q})")
        d = last + 1
    cost[v] = total
    if not parts:
        rec.step(f"v = 1 has no d from 2 up to v, so cost(1) is just 1.", t=table(v))
        continue
    words = " + ".join(parts)
    rec.step(
        f"cost({v}) = {v} + {words} = {total}."
        + (f" Every `{v} // d` is itself a value of `{n} // d`, so the table already holds it."
           if v == values[1] else ""),
        t=table(v)
    )
rec.step(
    f"The table is full. cost({n}) = {cost[n]} came from {len(values)} "
    f"entr{'ies' if len(values) != 1 else 'y'}, not from a table with {n} slots.",
    t=table()
)
rec.output(f"{len(values)}\n{cost[n]}\n")
