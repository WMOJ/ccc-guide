import vizrec as vz

rec = vz.Recorder()
data = rec.stdin.split()
n = int(data[0])
jobs = []
for k in range(n):
    jobs.append((data[1 + 3 * k], int(data[2 + 3 * k]), int(data[3 + 3 * k])))


def cost(order):
    clock = 0
    total = 0
    for name, t, w in order:
        clock += t
        total += w * clock
    return total


def cells(order):
    return [f"{name}{t}:{w}" for name, t, w in order]


cur = list(jobs)
now = cost(cur)
rec.step(
    "Each cell is a job: its letter, then time:weight. The schedule runs left to right, and in "
    f"this order the total cost is {now}. The plan is to fix one adjacent pair at a time.",
    order=vz.array(cells(cur)),
)
swaps = 0
for end in range(n - 1, 0, -1):
    moved = False
    for i in range(end):
        x, y = cur[i], cur[i + 1]
        lhs = x[1] * y[2]
        rhs = y[1] * x[2]
        pair = f"{x[0]} and {y[0]}"
        if lhs > rhs:
            cur[i], cur[i + 1] = y, x
            new = cost(cur)
            swaps += 1
            rec.step(
                f"{pair}: {x[1]} x {y[2]} = {lhs} is more than {y[1]} x {x[2]} = {rhs}, so {y[0]} "
                f"belongs first. Swapping lowers the total from {now} to {new}.",
                order=vz.array(
                    cells(cur),
                    states={i: "compare", i + 1: "compare"},
                    compare=(i, i + 1, f"-{now - new}"),
                ),
            )
            now = new
            moved = True
        else:
            note = "equal, so swapping changes nothing" if lhs == rhs else "already in order"
            rec.step(
                f"{pair}: {x[1]} x {y[2]} = {lhs} is at most {y[1]} x {x[2]} = {rhs}, {note}. "
                f"The total stays {now}.",
                order=vz.array(cells(cur), states={i: "done", i + 1: "done"}),
            )
    if not moved:
        break

order = [j[0] for j in cur]
rec.step(
    f"No adjacent pair is out of order. After {swaps} swaps the order is {' '.join(order)} and "
    f"the total is {now}. No swap ever raised it, so any starting order ends here.",
    order=vz.array(cells(cur)),
)
rec.output(" ".join(order) + "\n" + str(now) + "\n")
