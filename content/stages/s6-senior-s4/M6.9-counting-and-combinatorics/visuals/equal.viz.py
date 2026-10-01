import vizrec as vz

rec = vz.Recorder()
data = rec.stdin.split()
n = int(data[0])
readings = list(map(int, data[1:1 + n]))

order = []
for v in readings:
    if v not in order:
        order.append(v)
rows = len(order)
counts = {}
pairs_of = {}
running = {}


def table(current=None, phase=1):
    cells = []
    states = {}
    for r, v in enumerate(order):
        c = counts.get(v)
        p = pairs_of.get(v)
        t = running.get(v)
        cells.append([c, p, t])
        if current == v:
            for col in range(3):
                if cells[r][col] is not None:
                    states[(r, col)] = "current"
        elif p is not None:
            for col in range(3):
                states[(r, col)] = "done"
    return vz.table(cells, states=states, row_heads=[f"value {v}" for v in order],
                    col_heads=["count", "pairs", "total"])


def array(i, all_done=False):
    states = []
    for j in range(n):
        if all_done or j < i:
            states.append("done")
        elif j == i:
            states.append("current")
        else:
            states.append("none")
    ptr = [("next", i)] if i is not None and i < n else None
    return vz.array(readings, states=states, pointers=ptr, indices=True)


for i, v in enumerate(readings):
    counts[v] = counts.get(v, 0) + 1
    rec.step(
        f"Reading {i} is {v}, so the count for value {v} becomes {counts[v]}.",
        a=array(i), t=table(current=v),
    )

total = 0
for v in order:
    k = counts[v]
    p = k * (k - 1) // 2
    total += p
    pairs_of[v] = p
    running[v] = total
    if k == 1:
        why = f"Value {v} appears once, so it has nobody to pair with: 0 pairs."
    else:
        why = f"Value {v} appears {k} times, so it forms {k} * {k - 1} / 2 = {p} {'pair' if p == 1 else 'pairs'}."
    rec.step(f"{why} The running total is {total}.", a=array(n, True), t=table(current=v))

rec.step(
    f"Every pair of equal readings sits inside exactly one row, so the answer is {total}. "
    f"Testing all {n * (n - 1) // 2} pairs one by one would give the same number.",
    a=array(n, True), t=table(),
)
rec.output(f"{total}\n")
