import vizrec as vz

rec = vz.Recorder()
first = rec.readline().split()
n, trips = int(first[0]), int(first[1])
weights = [int(x) for x in rec.readline().split()]


def trips_for(cap):
    used = 1
    load = 0
    for w in weights:
        if load + w > cap:
            used += 1
            load = w
        else:
            load += w
    return used


lo0 = max(weights)
hi0 = sum(weights)
candidates = list(range(lo0, hi0 + 1))
feasible = [trips_for(c) <= trips for c in candidates]


def frame(lo, hi, mid=None):
    states = []
    for c, ok in zip(candidates, feasible):
        if c < lo or c > hi:
            states.append("_")
        else:
            states.append("d" if ok else "x")
    pointers = [("lo", candidates.index(lo), "below"), ("hi", candidates.index(hi), "below")]
    if mid is not None:
        pointers.append(("mid", candidates.index(mid), "above", True))
    return {"cap": vz.array(candidates, states=states, pointers=pointers)}


rec.step(
    f"Every capacity from the heaviest package, {lo0}, to carrying everything in one trip, "
    f"{hi0}, is a candidate. A capacity needing at most {trips} trips is feasible (marked done); "
    f"one needing more is not (marked invalid).",
    **frame(lo0, hi0),
)

lo, hi = lo0, hi0
while lo < hi:
    mid = (lo + hi) // 2
    need = trips_for(mid)
    if need <= trips:
        rec.step(
            f"Capacity {mid} needs {need} trip(s), at most {trips}. It is feasible, so the "
            f"answer could be {mid} or smaller: `hi` moves to {mid}.",
            **frame(lo, hi, mid),
        )
        hi = mid
    else:
        rec.step(
            f"Capacity {mid} needs {need} trips, more than {trips}. It is not feasible, so "
            f"`lo` moves to {mid + 1}.",
            **frame(lo, hi, mid),
        )
        lo = mid + 1

rec.step(
    f"`lo` and `hi` meet at {lo}. Every smaller capacity is infeasible and every capacity from "
    f"here up is feasible, so {lo} is the smallest capacity that still works.",
    **frame(lo, lo),
)

rec.output(f"{lo}\n")
