import vizrec as vz

rec = vz.Recorder()
n = int(rec.readline())
temps = [int(x) for x in rec.readline().split()]

pops_col = [""] * n
pushes_col = [""] * n
sum_push = [""] * n
sum_pop = [""] * n


def table(current=None):
    cells = [[temps[i], pops_col[i], pushes_col[i], sum_pop[i], sum_push[i]] for i in range(n)]
    states = ["_____"] * n
    if current is not None:
        states[current] = "ccccc"
    return vz.table(
        cells,
        states=states,
        row_heads=[str(i) for i in range(n)],
        col_heads=["temp", "pops", "push", "Σpops", "Σpush"],
        row_title="day",
    )


wait = [0] * n
stack = []
total_pops = 0
total_pushes = 0
for i in range(n):
    pops = 0
    while stack and temps[stack[-1]] < temps[i]:
        day = stack.pop()
        wait[day] = i - day
        pops += 1
    stack.append(i)
    total_pops += pops
    total_pushes += 1
    pops_col[i] = pops
    pushes_col[i] = 1
    sum_pop[i] = total_pops
    sum_push[i] = total_pushes
    if pops == 0:
        what = "pops nothing"
    elif pops == 1:
        what = "pops 1 day"
    else:
        what = f"pops {pops} days at once"
    rec.step(
        f"Day {i} ({temps[i]}) {what} and is pushed once. Totals so far: {total_pops} "
        f"{'pop' if total_pops == 1 else 'pops'} and {total_pushes} "
        f"{'push' if total_pushes == 1 else 'pushes'}."
        + (" `pops` counts the days popped, `push` the day pushed; the last two columns are "
           "running totals." if i == 0 else ""),
        t=table(i),
    )

rec.step(
    f"Finished: {total_pushes} pushes and {total_pops} pops, {total_pushes + total_pops} stack "
    f"operations for {n} days. Pops can never exceed pushes, since a day is popped at most once, "
    f"so the total stays under 2 x {n} = {2 * n} however the temperatures fall.",
    t=table(),
)
rec.output(" ".join(str(w) for w in wait) + "\n")
