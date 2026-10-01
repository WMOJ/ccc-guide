import random
import vizrec as vz

rec = vz.Recorder()
data = rec.stdin.split()
kind = data[0]
random.seed(int(data[1]))
sizes = [int(t) for t in data[2:]]


def comparisons(values, rank, use_random):
    work = 0
    while True:
        if use_random:
            pivot = values[random.randrange(len(values))]
        else:
            pivot = values[0]
        work += len(values)
        smaller = [v for v in values if v < pivot]
        larger = [v for v in values if v > pivot]
        equal = len(values) - len(smaller) - len(larger)
        if rank < len(smaller):
            values = smaller
        elif rank < len(smaller) + equal:
            return work
        else:
            rank -= len(smaller) + equal
            values = larger


rows = []
out_lines = []
for n in sizes:
    values = list(range(n))
    if kind == "shuffled":
        random.shuffle(values)
    elif kind == "equal":
        values = [7] * n
    first = comparisons(values, n // 2, False)
    rand = comparisons(values, n // 2, True)
    rows.append((n, first, rand))
    out_lines.append(f"n = {n}: first-element pivot {first}, random pivot {rand}")


def frame(upto):
    cells = []
    states = {}
    for r in range(len(rows)):
        if r <= upto:
            cells.append([rows[r][1], rows[r][2]])
            states[(r, 0)] = "current" if r == upto else "done"
            states[(r, 1)] = "current" if r == upto else "done"
        else:
            cells.append([None, None])
    return vz.table(
        cells, states=states, row_heads=[r[0] for r in rows],
        col_heads=["first pivot", "random pivot"], row_title="n", col_title="comparisons",
    )


for i, (n, first, rand) in enumerate(rows):
    if i == 0:
        caption = (
            f"For n = {n}, finding the middle value compares {first} times with the "
            f"first-element pivot and {rand} times with a random pivot."
        )
    else:
        pn, pf, pr = rows[i - 1]
        caption = (
            f"n doubles to {n}. The first-element pivot now compares {first} times, "
            f"{first / pf:.1f} times the previous row. The random pivot compares {rand} times, "
            f"{rand / pr:.1f} times the previous row."
        )
    rec.step(caption, t=frame(i))

rec.output("\n".join(out_lines) + "\n")
