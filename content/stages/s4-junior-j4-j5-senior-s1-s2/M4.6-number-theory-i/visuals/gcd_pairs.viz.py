import vizrec as vz

rec = vz.Recorder()
tokens = rec.stdin.split()
a = int(tokens[0])
b = int(tokens[1])


def shared(x, y):
    """Every number that divides both x and y (every divisor of x when y is 0)."""
    return [d for d in range(1, max(x, y) + 1) if x % d == 0 and y % d == 0]


def show(values):
    return " ".join(str(v) for v in values)


x, y = a, b
rows = []


def frame():
    cells = [[r[0], r[1], show(r[3])] for r in rows]
    states = []
    for i in range(len(rows)):
        states.append(["current"] * 3 if i == len(rows) - 1 else ["done"] * 3)
    return vz.table(
        cells,
        states=states,
        col_heads=["a", "b", "shared"],
        row_title="pair",
    )


def remainder_cell(p, q):
    return p % q if q != 0 else "-"


rows.append((x, y, remainder_cell(x, y), shared(x, y)))
rec.step(
    f"Start with the pair ({x}, {y}). The numbers that divide both are {show(shared(x, y))}; "
    "the largest of them is the gcd.",
    table=frame(),
)

while y != 0:
    old_x, old_y = x, y
    x, y = old_y, old_x % old_y
    rows.append((x, y, remainder_cell(x, y), shared(x, y)))
    if y != 0:
        rec.step(
            f"{old_x} % {old_y} = {y}, so ({x}, {y}) replaces ({old_x}, {old_y}). "
            f"A number dividing both {old_x} and {old_y} also divides {y}, and the reverse holds, "
            f"so the shared list is still {show(shared(x, y))}.",
            table=frame(),
        )
    else:
        rec.step(
            f"{old_x} % {old_y} = 0, so ({x}, 0) replaces ({old_x}, {old_y}). Every number divides 0, "
            f"so the shared divisors are just the divisors of {x}: {show(shared(x, y))}.",
            table=frame(),
        )

lcm = a * b // x
rec.step(
    f"The second number is 0, so the largest shared divisor is the first number: gcd = {x}. "
    f"The lcm follows: {a} * {b} // {x} = {lcm}.",
    table=frame(),
)
rec.output(f"{x}\n{lcm}\n")
