import vizrec as vz

rec = vz.Recorder()
data = rec.stdin.split()
n = int(data[0])
jobs = []
for k in range(n):
    jobs.append((data[1 + 3 * k], int(data[2 + 3 * k]), int(data[3 + 3 * k])))

(pn, pt, pw), (xn, xt, xw), (yn, yt, yw) = jobs
s = pt
end = s + xt + yt
names = [pn, xn, yn]


def table(states):
    return vz.table(
        [[pt, xt, yt], [pw, xw, yw]], states=states, row_heads=["t", "w"], col_heads=names
    )


cost_xy = xw * (s + xt) + yw * (s + xt + yt)
cost_yx = yw * (s + yt) + xw * (s + yt + xt)
wait_x = yw * xt
wait_y = xw * yt
delta = cost_xy - cost_yx

before = [
    (0, s, pn, "done", 0),
    (s, s + xt, xn, "compare", 0),
    (s + xt, end, yn, "compare", 0),
]
after = [
    (0, s, pn, "done", 1),
    (s, s + yt, yn, "compare", 1),
    (s + yt, end, xn, "compare", 1),
]

rec.step(
    f"{pn} runs first and stays put. Then {xn} finishes at {s + xt} and {yn} at {end}. "
    f"The pair pays {xw} x {s + xt} + {yw} x {end} = {cost_xy} together.",
    t=table(["_cc", "_cc"]),
    line=vz.line(0, end, tick=1, intervals=before),
)
rec.step(
    f"Swap {xn} and {yn}. {yn} now finishes at {s + yt} and {xn} at {end}, so the pair pays "
    f"{yw} x {s + yt} + {xw} x {end} = {cost_yx}. Top row: before. Bottom row: after.",
    t=table(["_cc", "_cc"]),
    line=vz.line(0, end, tick=1, intervals=before + after),
)
if delta > 0:
    verdict = f"The swap is {delta} cheaper, so {yn} should go first."
elif delta == 0:
    verdict = "The swap changes nothing, so either order is fine."
else:
    verdict = f"The swap is {-delta} dearer, so {xn} first is the better order."
rec.step(
    f"Why: {xn} first makes {yn} wait {xt} min, costing {yw} x {xt} = {wait_x}. {yn} first "
    f"makes {xn} wait {yt} min, costing {xw} x {yt} = {wait_y}. {pn}'s {s} minutes delay both orders "
    f"alike. {verdict}",
    t=table(["_cc", "_cc"]),
    line=vz.line(0, end, tick=1, intervals=before + after),
)

ranked = sorted(jobs, key=lambda j: (j[1] / j[2], j[0], j[1], j[2]))
clock = 0
total = 0
for name, t, w in ranked:
    clock += t
    total += w * clock
rec.output(" ".join(j[0] for j in ranked) + "\n" + str(total) + "\n")
