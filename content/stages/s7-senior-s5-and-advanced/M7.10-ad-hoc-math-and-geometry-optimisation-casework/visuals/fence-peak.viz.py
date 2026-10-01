import vizrec as vz

rec = vz.Recorder()
data = rec.stdin.split()
w = int(data[0])
limit = int(data[1])
hi = min(limit, (w - 1) // 2)
full = (w - 1) // 2
xs = list(range(1, full + 1))
areas = [x * (w - 2 * x) for x in xs]
peak = max(areas)
ticks = sorted(set([1, full, full // 2, full // 4 if full >= 4 else 1]))


def chart(marks=None, vline=None, band=None):
    return vz.plot(
        x=(1, max(full, 2), "x, side length", ticks[:8]),
        y=(0, peak + peak // 10 + 1, "area"),
        series=[("a", "area", list(zip(xs, areas)), 0)],
        markers=marks,
        vline=vline,
        band=band,
    )


rec.step(
    f"{w} meters of wire fence a rectangle against a long wall. Two sides of length x and one "
    f"of length {w} - 2x need wire, so the area is x * ({w} - 2x). Each x from 1 to {full} is "
    f"one case; the curve shows them all.",
    plot=chart(),
)
if hi < full:
    rec.step(
        f"A shed restricts x to at most {hi}. The shaded band is the allowed range; cases to "
        "its right are off the table.",
        plot=chart(band=(1, hi, "allowed")),
    )
vertex = w / 4
rec.step(
    f"Area is -2x^2 + {w}x, a parabola that opens downward, so its peak is at x = {w}/4 = "
    f"{vertex:g}. Whole numbers only, so the peak is not always a case.",
    plot=chart(vline=(vertex, "peak"), band=(1, hi, "allowed") if hi < full else None),
)
low = w // 4
picks = []
for pick in (low, low + 1):
    x = max(1, min(hi, pick))
    if x not in [p[0] for p in picks]:
        picks.append((x, x * (w - 2 * x)))
marks = [(x, a, f"x={x}", "current") for x, a in picks]
best_x, best_area = picks[0]
for x, a in picks:
    if a > best_area:
        best_x, best_area = x, a
if hi < low:
    why = f"The peak at {vertex:g} lies beyond the allowed range, so the clamp pulls both candidates to x = {hi}."
else:
    why = f"The two whole numbers beside the peak, {low} and {low + 1}, are the only candidates."
if len(picks) == 1:
    tail = f"Both land on x = {best_x}, area {best_area}."
elif picks[0][1] == picks[1][1]:
    tail = f"Their areas tie at {best_area}, so x = {best_x} stays."
else:
    tail = "Their areas: " + ", ".join(f"{a} at x = {x}" for x, a in picks) + f". The larger is {best_area} at x = {best_x}."
rec.step(
    f"{why} {tail}",
    plot=chart(marks=marks, vline=(vertex, "peak"), band=(1, hi, "allowed") if hi < full else None),
)
rec.output(f"{best_x} {best_area}\n")
