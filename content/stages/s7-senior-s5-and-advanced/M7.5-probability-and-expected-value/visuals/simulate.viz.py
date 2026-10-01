import math
import random

import vizrec as vz

rec = vz.Recorder()
n, p_text, seed = rec.readline().split()
n = int(n)
p = float(p_text)
rng = random.Random(int(seed))

# Exact answer by the backward recurrence.
q = 1 - p
e = [0.0] * (n + 2)
for i in range(n - 1, -1, -1):
    e[i] = 1 + p * e[i + 1] + q * e[i + 2]
exact = e[0]

marks = [10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000]
pts = []
total = 0
games = 0
lines = []
reports = {}
for limit in marks:
    while games < limit:
        square = 0
        while square < n:
            if rng.random() < p:
                square += 1
            else:
                square += 2
            total += 1
        games += 1
    avg = total / games
    pts.append((round(math.log10(limit), 3), round(avg, 3)))
    reports[limit] = avg
    if limit in (10, 100, 1000, 10000):
        lines.append(f"after {limit} games: {avg:.3f}")

lo = 2.0
hi = 3.0


def frame(upto):
    shown = [pt for pt, m in zip(pts, marks) if m <= upto]
    series = [
        ("avg", "average", shown, 0),
        ("exact", "exact", [(1, exact), (4, exact)], 1),
    ]
    last = shown[-1]
    return vz.plot(
        x=(1, 4, "games, as a power of 10", [1, 2, 3, 4]),
        y=(lo, hi, "turns per game"),
        series=series,
        markers=[(last[0], last[1], f"{last[1]:.2f}", "c")],
    )


rec.step(
    f"Play the game 10 times with a seeded random coin and average the turns. The average is {reports[10]:.3f}. "
    f"The dashed line is the exact expected value of {exact:g}. Ten games are far too few to land near it.",
    p=frame(10),
)
rec.step(
    f"After 100 games the average is {reports[100]:.3f}. Each new game moves the average less "
    "because it is one more vote among many.",
    p=frame(100),
)
rec.step(
    f"After 1000 games the average is {reports[1000]:.3f}, off by {abs(reports[1000] - exact):.3f} from the exact value.",
    p=frame(1000),
)
rec.step(
    f"After 10000 games it is {reports[10000]:.3f}. The average settles toward {exact:g}. "
    "It remains a sample, so it carries noise that the exact computation does not have.",
    p=frame(10000),
)
rec.output("\n".join(lines) + "\n")
