import vizrec as vz

rec = vz.Recorder()
data = rec.stdin.split()
n = int(data[0])

forwards = list(range(1, n + 1))
backwards = list(range(n, 0, -1))
cols = [str(i) for i in range(1, n + 1)]


def frame(shown_back, shown_sums, current=None):
    row_f = forwards
    row_b = [backwards[i] if i < shown_back else None for i in range(n)]
    row_s = [forwards[i] + backwards[i] if i < shown_sums else None for i in range(n)]
    states = []
    for _ in range(3):
        states.append(["none"] * n)
    if current is not None:
        for r in range(3):
            states[r][current] = "current"
    return vz.table(
        [row_f, row_b, row_s],
        states=states,
        row_heads=["forwards", "backwards", "sum"],
        col_heads=cols,
    )


rec.step(
    f"Write the terms in a row: {' + '.join(str(v) for v in forwards)}. Their sum is what we want."
    if n > 1
    else "Write the single term, 1, in a row. Its sum is 1.",
    table=frame(0, 0),
)
rec.step(
    f"Write the same terms again in the second row, backwards ({n} down to 1). Both rows have the "
    "same sum, so together they add to twice the answer.",
    table=frame(n, 0),
)
for i in range(n):
    rec.step(
        f"Column {i + 1}: {forwards[i]} + {backwards[i]} = {forwards[i] + backwards[i]}, "
        f"the same as {n} + 1.",
        table=frame(n, i + 1, current=i),
    )
total = n * (n + 1) // 2
rec.step(
    f"{'All ' + str(n) + ' columns add' if n > 1 else 'The one column adds'} to {n + 1}, so both rows together total {n} * {n + 1} = {n * (n + 1)}. "
    f"One row alone is half: {n * (n + 1)} // 2 = {total}.",
    table=frame(n, n),
)
rec.output(f"{total}\n")
