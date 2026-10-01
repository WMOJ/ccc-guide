import vizrec as vz

rec = vz.Recorder()
n, p = (int(t) for t in rec.readline().split())
x = p / n
xs = [x]
ps = [p]
lines = []
for step in range(1, 61):
    x = 2 * min(x, 1 - x)
    p = 2 * min(p, n - p)
    xs.append(x)
    ps.append(p)
    if step % 10 == 0:
        lines.append(f"step {step}: float {x}, exact {p}/{n}")


def frame(upto):
    flt = [(k, round(xs[k], 4)) for k in range(upto + 1)]
    ext = [(k, round(ps[k] / n, 4)) for k in range(upto + 1)]
    return vz.plot(
        x=(0, 60, "steps", [0, 20, 40, 60]),
        y=(0, 1, "value"),
        series=[("exact", "exact p/n", ext, 0), ("float", "float", flt, 1)],
        markers=[(upto, round(xs[upto], 4), "float", "c")],
    )


rec.step(
    f"Both versions start at {ps[0]}/{n}. Each step replaces x by 2 * min(x, 1 - x). "
    f"The solid line keeps the integer numerator p over {n}, so each value is exact. "
    "The dashed line keeps a float. So far the two are the same.",
    c=frame(0),
)
rec.step(
    f"By step 10 the float reads {xs[10]:.16f} and the exact value is {ps[10]}/{n} = {ps[10] / n:.16f}. "
    "The plot cannot show the difference yet.",
    c=frame(10),
)
rec.step(
    f"By step 40 the float is {xs[40]:.6f} against {ps[40] / n:.6f}, off by {abs(xs[40] - ps[40] / n):.1e}. "
    "Each step doubles the rounding error left by the subtraction, so a change in the sixteenth digit "
    "has reached the sixth.",
    c=frame(40),
)
rec.step(
    f"At step 50 the float is {xs[50]:.5f}, visibly off {ps[50] / n:.5f}. "
    f"At step 60 it is {xs[60]:g}, stuck for good, while the exact numerator keeps cycling "
    f"through {ps[56]}, {ps[57]}, {ps[58]}, {ps[59]} and {ps[60]} over {n}.",
    c=frame(60),
)
rec.output("\n".join(lines) + "\n")
