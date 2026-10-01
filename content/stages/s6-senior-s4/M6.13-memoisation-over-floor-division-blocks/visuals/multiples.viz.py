import vizrec as vz

rec = vz.Recorder()
n = int(rec.readline())


def table(upto, current=None):
    cells = []
    states = {}
    for d in range(1, n + 1):
        row = []
        for i in range(1, n + 1):
            if d <= upto and i % d == 0:
                row.append("x")
                states[(d - 1, i - 1)] = "current" if d == current else "done"
            else:
                row.append("")
        cells.append(row)
    heads = [f"d={d}" for d in range(1, n + 1)]
    return vz.table(cells, states=states or None, row_heads=heads,
                    col_heads=[str(i) for i in range(1, n + 1)], col_title="i")


counts = [0] * (n + 1)
for d in range(1, n + 1):
    for i in range(d, n + 1, d):
        counts[i] += 1

rec.step(
    f"Row d has an x in column i when d divides i. Count the x marks in a column and you get "
    f"the number of divisors of i. The grid starts blank for n = {n}; rows fill in from d = 1.",
    t=table(0)
)
running = 0
for d in range(1, n + 1):
    running += n // d
    rec.step(
        f"d = {d} divides {', '.join(str(i) for i in range(d, n + 1, d))}: "
        f"{n // d} multiple{'s' if n // d != 1 else ''}, exactly `{n} // {d}`. Marks so far: {running}.",
        t=table(d, current=d)
    )
by_divisors = sum(counts[1:])
rec.step(
    f"The marks total {running}, which is the sum of the divisor counts of 1 to {n}: "
    f"{' + '.join(str(c) for c in counts[1:])} = {by_divisors}.",
    t=table(n)
)
rec.output(f"{by_divisors}\n{by_divisors}\n")
