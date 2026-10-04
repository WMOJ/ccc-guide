import vizrec as vz

rec = vz.Recorder()
data = rec.stdin.split()
n = int(data[0])
jobs = []
for k in range(n):
    jobs.append((data[1 + 3 * k], int(data[2 + 3 * k]), int(data[3 + 3 * k])))
span = max(sum(j[1] for j in jobs), max(j[2] for j in jobs))


def lateness(order):
    clock = 0
    out = []
    for name, t, d in order:
        clock += t
        out.append(clock - d)
    return out


def draw(order, hot=()):
    clock = 0
    ivs = []
    for name, t, d in order:
        state = "compare" if name in hot else ("invalid" if clock + t > d else "done")
        ivs.append((clock, clock + t, name, state, 0))
        clock += t
    pts = [(d, f"d{name}", "frontier") for name, t, d in order]
    return vz.line(0, span, tick=1, intervals=ivs, points=pts)


cur = list(jobs)
job_lateness = lateness(cur)
worst = max(job_lateness)
worst_name = cur[job_lateness.index(worst)][0]
start = worst
rec.step(
    "Jobs run left to right in input order. A marker dX is job X's deadline. Jobs drawn as late "
    f"miss it. The worst lateness is {worst}, on job {worst_name}"
    + ("." if worst > 0 else " (negative means early)."),
    line=draw(cur),
)
for end in range(n - 1, 0, -1):
    moved = False
    for i in range(end):
        x, y = cur[i], cur[i + 1]
        if x[2] > y[2]:
            before = max(lateness(cur)[i:i + 2])
            cur[i], cur[i + 1] = y, x
            after = max(lateness(cur)[i:i + 2])
            whole = max(lateness(cur))
            rec.step(
                f"{x[0]} (deadline {x[2]}) runs before {y[0]} (deadline {y[2]}), out of order. "
                f"Swapping them changes the pair's worst lateness from {before} to {after}. The "
                f"whole schedule's worst is now {whole}.",
                line=draw(cur, hot=(x[0], y[0])),
            )
            moved = True
        else:
            rec.step(
                f"{x[0]} (deadline {x[2]}) before {y[0]} (deadline {y[2]}) is already in "
                "deadline order, so this pair stays.",
                line=draw(cur, hot=(x[0], y[0])),
            )
    if not moved:
        break

final = max(lateness(cur))
rec.step(
    f"Deadline order is {' '.join(j[0] for j in cur)}. Its worst lateness is {final}, "
    + (f"down from {start}" if final < start else f"the same as the start")
    + ". No swap ever raised the worst lateness of the pair it touched.",
    line=draw(cur),
)
rec.output(" ".join(j[0] for j in cur) + "\n" + str(final) + "\n")
