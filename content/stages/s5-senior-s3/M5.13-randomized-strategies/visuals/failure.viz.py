import math
import vizrec as vz

rec = vz.Recorder()
data = rec.stdin.split()
digits = int(data[0])
target = 10.0 ** -digits
probs = [float(t) for t in data[1:]]

floor_y = -(digits + 1)
results = []
out_lines = []
for p in probs:
    failure = 1.0
    trials = 0
    while failure >= target:
        failure *= 1 - p
        trials += 1
    results.append((p, trials, failure))
    out_lines.append(f"p = {p}: {trials} trials, failure {failure:.1e}")


def end_of_line(p):
    return int(math.ceil(floor_y / math.log10(1 - p)))


x_max = max(end_of_line(p) for p in probs)
x_max = ((x_max + 9) // 10) * 10
ticks = [0, x_max // 2, x_max]
styles = [0, 2, 3]


def curve(p):
    step = max(1, end_of_line(p) // 100)
    pts = []
    failure = 1.0
    k = 0
    while k <= end_of_line(p):
        pts.append((k, max(floor_y, math.log10(failure))))
        for _ in range(step):
            failure *= 1 - p
        k += step
    return pts


def word(k):
    return "trial" if k == 1 else "trials"


series_all = []
for idx, (p, trials, failure) in enumerate(results):
    series_all.append(("p%d" % idx, f"p = {p}", curve(p), styles[idx]))
    series = [("target", "target", [(0, -digits), (x_max, -digits)], 1)] + list(series_all)
    if idx == 0:
        caption = (
            f"With p = {p}, a trial fails with probability {round(1 - p, 4)}, so k trials all fail "
            f"with probability {round(1 - p, 4)}^k. On this exponent scale that is a straight line. "
            f"It reaches the target, one in 10^{digits}, at {trials} {word(trials)}."
        )
    else:
        caption = (
            f"With p = {p}, each failure multiplies by {round(1 - p, 4)}, so the line falls "
            f"{'more slowly' if p < results[idx - 1][0] else 'faster'}. It crosses the target at "
            f"{trials} {word(trials)}."
        )
    rec.step(
        caption,
        p=vz.plot(
            (0, x_max, "trials k", ticks),
            (floor_y, 0, "log10 of failure"),
            series,
            
            vline=(trials, f"k = {trials}"),
        ),
    )

rec.output("\n".join(out_lines) + "\n")
