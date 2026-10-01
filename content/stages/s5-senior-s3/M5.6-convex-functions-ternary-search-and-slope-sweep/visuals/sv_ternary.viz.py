import vizrec as vz

rec = vz.Recorder()
n = int(rec.readline())
positions = [int(x) for x in rec.readline().split()]
weights = [int(x) for x in rec.readline().split()]
lo0, hi0 = [int(x) for x in rec.readline().split()]


def cost(c):
    total = 0
    for p, w in zip(positions, weights):
        total += w * abs(p - c)
    return total


curve = [(c, cost(c)) for c in range(lo0, hi0 + 1)]
y_max = max(v for _, v in curve)


def frame(lo, hi, m1=None, m2=None):
    markers = []
    if m1 is not None:
        markers.append((m1, cost(m1), "m1"))
    if m2 is not None:
        markers.append((m2, cost(m2), "m2"))
    return {
        "plot": vz.plot(
            x=(lo0, hi0, "location c"),
            y=(0, y_max, "cost(c)"),
            series=[("cost", "cost(c)", curve, 0)],
            markers=markers,
            band=(lo, hi, "searching"),
        )
    }


lo, hi = lo0, hi0
rec.step(
    f"cost(c) sums each job site's weight times its distance from c. It is convex: it only "
    f"decreases, then only increases, so the shaded band from {lo} to {hi} is the whole search space.",
    **frame(lo, hi),
)

while hi - lo > 2:
    m1 = lo + (hi - lo) // 3
    m2 = hi - (hi - lo) // 3
    c1, c2 = cost(m1), cost(m2)
    if c1 > c2:
        rec.step(
            f"cost({m1}) is {c1}, more than cost({m2}) at {c2}. The minimum cannot be left of "
            f"{m1}: `lo` moves to {m1 + 1}.",
            **frame(lo, hi, m1, m2),
        )
        lo = m1 + 1
    else:
        rec.step(
            f"cost({m1}) is {c1}, at most cost({m2}) at {c2}. The minimum cannot be right of "
            f"{m2}: `hi` moves to {m2 - 1}.",
            **frame(lo, hi, m1, m2),
        )
        hi = m2 - 1

best_loc, best_cost = lo, cost(lo)
for c in range(lo + 1, hi + 1):
    c_cost = cost(c)
    if c_cost < best_cost:
        best_loc, best_cost = c, c_cost

rec.step(
    f"Only {hi - lo + 1} candidate(s) are left, few enough to check directly. "
    f"The minimum is at c = {best_loc}, cost {best_cost}.",
    **frame(best_loc, best_loc, None, None),
)

rec.output(f"{best_loc} {best_cost}\n")
