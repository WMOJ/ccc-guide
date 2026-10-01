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


def frame(lo, hi, mid=None):
    markers = []
    if mid is not None:
        markers.append((mid, cost(mid), "f(mid)"))
        markers.append((mid + 1, cost(mid + 1), "f(mid+1)"))
    return {
        "plot": vz.plot(
            x=(lo0, hi0, "location c"),
            y=(0, y_max, "cost(c)"),
            series=[("cost", "cost(c)", curve, 0)],
            markers=markers,
            band=(lo, hi, "searching"),
        )
    }


def past_the_minimum(x):
    return cost(x + 1) - cost(x) >= 0


lo, hi = lo0, hi0
rec.step(
    f"The same curve, searched a different way: compare cost at `mid` and `mid + 1` instead of "
    f"two interior thirds.",
    **frame(lo, hi),
)

while lo < hi:
    mid = (lo + hi) // 2
    delta = cost(mid + 1) - cost(mid)
    if delta >= 0:
        rec.step(
            f"cost({mid + 1}) minus cost({mid}) is {delta}, at least 0: the curve is flat or "
            f"rising here. The minimum is at or before {mid}: `hi` moves to {mid}.",
            **frame(lo, hi, mid),
        )
        hi = mid
    else:
        rec.step(
            f"cost({mid + 1}) minus cost({mid}) is {delta}, negative: the curve is still "
            f"falling here. The minimum is after {mid}: `lo` moves to {mid + 1}.",
            **frame(lo, hi, mid),
        )
        lo = mid + 1

rec.step(
    f"`lo` and `hi` meet at {lo}, the first point where the curve stops falling: cost = {cost(lo)}.",
    **frame(lo, lo),
)

rec.output(f"{lo} {cost(lo)}\n")
