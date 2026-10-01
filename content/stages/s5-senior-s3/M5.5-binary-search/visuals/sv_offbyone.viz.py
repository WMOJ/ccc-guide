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
    hi_shown = min(hi, hi0)
    states = []
    for c, ok in zip(candidates, feasible):
        if c < lo or c > hi_shown:
            states.append("_")
        else:
            states.append("d" if ok else "x")
    pointers = [("lo", candidates.index(lo), "below"), ("hi", candidates.index(hi_shown), "below")]
    if mid is not None:
        pointers.append(("mid", candidates.index(mid), "above", True))
    return vz.array(candidates, states=states, pointers=pointers)


lo_c, hi_c = lo0, hi0
lo_b, hi_b = lo0, hi0
done_c = False
done_b = False

rec.step(
    f"Both searches start with the same candidates, {lo0} to {hi0}. One will update `hi = mid`, "
    f"the other `hi = mid - 1`, whenever a mid is feasible.",
    correct=frame(lo_c, hi_c),
    broken=frame(lo_b, hi_b),
)

while not (done_c and done_b):
    if lo_c < hi_c:
        mid_c = (lo_c + hi_c) // 2
        need_c = trips_for(mid_c)
    else:
        mid_c = None
        done_c = True
    if lo_b < hi_b:
        mid_b = (lo_b + hi_b) // 2
        need_b = trips_for(mid_b)
    else:
        mid_b = None
        done_b = True

    if mid_c is None and mid_b is None:
        break

    parts = []
    if mid_c is not None:
        if need_c <= trips:
            parts.append(f"correct: mid {mid_c} needs {need_c} trips, feasible, so `hi = mid` moves `hi` to {mid_c}.")
            hi_c = mid_c
        else:
            parts.append(f"correct: mid {mid_c} needs {need_c} trips, not feasible, so `lo` moves to {mid_c + 1}.")
            lo_c = mid_c + 1
    else:
        parts.append(f"correct: already settled at {lo_c}.")

    if mid_b is not None:
        if need_b <= trips:
            parts.append(
                f"broken: mid {mid_b} needs {need_b} trips, feasible, but `hi = mid - 1` throws it away, "
                f"moving `hi` to {mid_b - 1} instead of keeping it at {mid_b}."
            )
            hi_b = mid_b - 1
        else:
            parts.append(f"broken: mid {mid_b} needs {need_b} trips, not feasible, so `lo` moves to {mid_b + 1}.")
            lo_b = mid_b + 1
    else:
        parts.append(f"broken: already settled at {lo_b}.")

    rec.step(" ".join(parts), correct=frame(lo_c, hi_c, mid_c), broken=frame(lo_b, hi_b, mid_b))

need_b_final = trips_for(lo_b)
rec.step(
    f"`lo` and `hi` meet at {lo_c} in the correct search, the true smallest feasible capacity "
    f"(`trips_for({lo_c})` is {trips_for(lo_c)}, at most {trips}). The broken search meets at "
    f"{lo_b}, but `trips_for({lo_b})` is {need_b_final}, more than {trips}: it stopped on a "
    f"capacity that does not actually work.",
    correct=frame(lo_c, lo_c),
    broken=frame(lo_b, lo_b),
)

rec.output(f"{lo_c}\n")
