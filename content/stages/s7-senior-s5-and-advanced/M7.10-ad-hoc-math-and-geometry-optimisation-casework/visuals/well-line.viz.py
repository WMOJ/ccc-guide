import vizrec as vz

rec = vz.Recorder()
data = rec.stdin.split()
n = int(data[0])
houses = sorted(int(v) for v in data[1:n + 1])
top = houses[-1] + 1
prefix = [0]
for h in houses:
    prefix.append(prefix[-1] + h)


def cost_at(p):
    return sum(abs(h - p) for h in houses)


def pts(p=None):
    out = []
    for h in houses:
        if p is None:
            out.append((h, None, None))
        else:
            out.append((h, str(abs(h - p)), "current" if h == p else None))
    return out


rec.step(
    f"{n} house{'s' if n != 1 else ''} stand{'' if n != 1 else 's'} along a road at the marked position{'s' if n != 1 else ''}. A well goes at a whole-number spot, "
    "and the cost is the total walking distance from every house to it. Checking every spot costs "
    "a full pass over the houses each time, so look for a short list of spots to check.",
    road=vz.line(0, top, tick=1, points=pts()),
)

best_at = None
best_cost = None
for i, h in enumerate(houses):
    left = h * i - prefix[i]
    right = prefix[n] - prefix[i + 1] - h * (n - 1 - i)
    total = left + right
    if best_cost is None or total < best_cost:
        best_at, best_cost = h, total
        verdict = f"New best: {total} at {h}."
    else:
        verdict = f"Best stays {best_cost} at {best_at}."
    rec.step(
        f"Well at house {h}. Left: {h} x {i} - {prefix[i]} = {left}. Right: "
        f"{prefix[n] - prefix[i + 1]} - {h} x {n - 1 - i} = {right}. Total {total}. {verdict} "
        "Labels show each house's distance.",
        road=vz.line(0, top, tick=1, points=pts(h), sweep=(h, "well")),
    )

gap = None
for i in range(n - 1):
    if houses[i + 1] - houses[i] >= 2:
        gap = i
        break
if gap is not None:
    a, b = houses[gap], houses[gap + 1]
    p = a + 1
    ca, cb, cp = cost_at(a), cost_at(b), cost_at(p)
    rec.step(
        f"What about a spot between houses, like {p}? Its cost is {cp}, between the neighbors' {ca} "
        f"and {cb}. Between two houses each step right adds the same amount, so the cost runs "
        "along a straight line and an end is never worse.",
        road=vz.line(0, top, tick=1, points=pts(), sweep=(p, "between")),
    )

rec.step(
    f"Only the {n} house position{'s' if n != 1 else ''} need{'' if n != 1 else 's'} checking. The cheapest is {best_cost} with the well at "
    f"{best_at}.",
    road=vz.line(0, top, tick=1, points=pts(best_at), sweep=(best_at, "well")),
)
rec.output(f"{best_at} {best_cost}\n")
