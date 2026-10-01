import vizrec as vz

rec = vz.Recorder()
data = rec.stdin.split()
n = int(data[0])
jobs = []
for k in range(n):
    jobs.append((data[1 + 3 * k], int(data[2 + 3 * k]), int(data[3 + 3 * k])))
names = [j[0] for j in jobs]


def table():
    return vz.table(
        [[j[1] for j in jobs], [j[2] for j in jobs], [f"{j[1] / j[2]:g}" for j in jobs]],
        row_heads=["t", "w", "t/w"],
        col_heads=names,
    )


def schedule(order, row):
    clock = 0
    cost = 0
    ivs = []
    parts = []
    for name, t, w in order:
        start = clock
        clock += t
        cost += w * clock
        ivs.append((start, clock, name, "compare" if row == 0 else "done", row))
        parts.append(f"{name} {w}x{clock}={w * clock}")
    return cost, ivs, parts


by_time = sorted(jobs, key=lambda j: (j[1], j[0]))
by_ratio = sorted(jobs, key=lambda j: (j[1] / j[2], j[0]))
total = sum(j[1] for j in jobs)
cost_a, ivs_a, parts_a = schedule(by_time, 0)
cost_b, ivs_b, parts_b = schedule(by_ratio, 1)

rec.step(
    "Key one: shortest job first, the rule from M4.2. Each job pays its weight times its finish "
    f"time: {', '.join(parts_a)}. Total {cost_a}.",
    t=table(),
    line=vz.line(0, total, tick=1, intervals=ivs_a),
)
rec.step(
    "Key two: smallest t/w first. Same jobs, new order on the bottom row: "
    f"{', '.join(parts_b)}. Total {cost_b}.",
    t=table(),
    line=vz.line(0, total, tick=1, intervals=ivs_a + ivs_b),
)
if [j[0] for j in by_time] == [j[0] for j in by_ratio]:
    rec.step(
        f"Both keys give the order {' '.join(j[0] for j in by_time)} here, because every job has "
        f"weight {jobs[0][2]}. The keys only part ways when weights differ.",
        t=table(),
        line=vz.line(0, total, tick=1, intervals=ivs_a + ivs_b),
    )
else:
    heavy = max(jobs, key=lambda j: j[2])
    rec.step(
        f"Shortest first costs {cost_a}, t/w costs {cost_b}. Job {heavy[0]} has the largest weight "
        f"({heavy[2]}), so each minute it waits is expensive, and t/w moves it forward. Time "
        "alone ignores weight.",
        t=table(),
        line=vz.line(0, total, tick=1, intervals=ivs_a + ivs_b),
    )

rec.output(" ".join(j[0] for j in by_ratio) + "\n" + str(cost_b) + "\n")
