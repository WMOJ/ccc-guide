import vizrec as vz

rec = vz.Recorder()
n, trips = map(int, rec.readline().split())
weights = list(map(int, rec.readline().split()))


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
lo, hi = lo0, hi0
span = list(range(lo0, hi0 + 1))


def frame(mid=None, dead_lo=None, dead_hi=None):
    states = []
    for cap in span:
        if cap < lo or cap > hi:
            states.append("x")
        elif cap == mid:
            states.append("c")
        else:
            states.append("_")
    ptrs = [("lo", lo - lo0, "above"), ("hi", hi - lo0, "below")]
    if mid is not None:
        ptrs.append(("mid", mid - lo0, "above"))
    return {"arr": vz.array(span, states="".join(states), pointers=ptrs, name="capacity")}


rec.step(
    f"The answer is a capacity. It is at least the heaviest weight, {lo0}, and at most the total, {hi0}. "
    f"lo = {lo} and hi = {hi} mark the two ends of the candidates. Greyed capacities are already ruled out.",
    **frame(),
)
while lo < hi:
    mid = (lo + hi) // 2
    need = trips_for(mid)
    if need <= trips:
        rec.step(
            f"mid = ({lo} + {hi}) // 2 = {mid}. A capacity of {mid} needs {need} "
            f"{'trip' if need == 1 else 'trips'}, which is at most {trips}, so {mid} works. "
            f"Keep it and look lower: hi = {mid}.",
            **frame(mid),
        )
        hi = mid
    else:
        rec.step(
            f"mid = ({lo} + {hi}) // 2 = {mid}. A capacity of {mid} needs {need} trips, more than {trips}, "
            f"so {mid} fails and so does everything below it. lo = {mid + 1}.",
            **frame(mid),
        )
        lo = mid + 1
rec.step(
    f"lo and hi are both {lo}, so one candidate is left. The smallest capacity that works is {lo}.",
    **frame(),
)
rec.output(f"{lo}\n")
