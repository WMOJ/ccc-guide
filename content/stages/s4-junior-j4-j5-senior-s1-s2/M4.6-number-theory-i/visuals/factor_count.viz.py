import vizrec as vz

rec = vz.Recorder()
tokens = rec.stdin.split()
n = int(tokens[0])

rows = [("start", "-", "-", 1)]


def frame():
    cells = [[r[1], r[2], r[3]] for r in rows]
    states = []
    for i in range(len(rows)):
        states.append(["current"] * 3 if i == len(rows) - 1 else ["done"] * 3)
    return vz.table(
        cells,
        states=states,
        row_heads=[r[0] for r in rows],
        col_heads=["exponent", "choices", "divisors"],
        row_title="prime",
    )


rec.step(
    f"Factor {n}. The row for each prime will show its exponent, the choices it gives a divisor "
    "(0 up to the exponent), and the divisor count so far, which starts at 1.",
    table=frame(),
)

remaining = n
count = 1
factors = []
p = 2
while p * p <= remaining:
    if remaining % p == 0:
        exponent = 0
        trail = [str(remaining)]
        while remaining % p == 0:
            remaining //= p
            exponent += 1
            trail.append(str(remaining))
        factors.append((p, exponent))
        before = count
        count *= exponent + 1
        rows.append((str(p), exponent, exponent + 1, count))
        rec.step(
            f"{p} divides evenly {exponent} time{'s' if exponent > 1 else ''}: {' -> '.join(trail)}. "
            f"A divisor holds between 0 and {exponent} copies of {p}: {exponent + 1} choices. "
            f"Divisors so far: {before} * {exponent + 1} = {count}.",
            table=frame(),
        )
    else:
        rec.step(
            f"{p} does not divide {remaining}. Try the next candidate while {p} * {p} is at most "
            f"{remaining}.",
            table=frame(),
        )
    p += 1

if remaining > 1:
    factors.append((remaining, 1))
    before = count
    count *= 2
    rows.append((str(remaining), 1, 2, count))
    rec.step(
        f"The loop stops because {p} * {p} is more than {remaining}. What is left, {remaining}, "
        f"is a prime with exponent 1: 2 choices. Divisors so far: {before} * 2 = {count}.",
        table=frame(),
    )

parts = [f"{q}^{e}" for q, e in factors]
rec.step(
    f"{n} = {' * '.join(parts)}, so it has {count} divisors, the product of the choices.",
    table=frame(),
)
rec.output(" ".join(parts) + "\n" + str(count) + "\n")
