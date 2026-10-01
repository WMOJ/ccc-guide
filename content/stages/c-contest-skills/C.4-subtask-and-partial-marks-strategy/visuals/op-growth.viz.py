import vizrec as vz

rec = vz.Recorder()
k = int(rec.readline())
bound = int(rec.readline().split()[0])

BUDGET = 10**7


def counts(n):
    return n * (n + 1) * (n + 2) // 6, n * (n + 1) // 2, n


def counted(n):
    cubic = quadratic = 0
    for i in range(n):
        for j in range(i, n):
            quadratic += 1
            for _ in range(i, j + 1):
                cubic += 1
    return cubic, quadratic, n


for probe in range(1, 40):
    assert counts(probe) == counted(probe)

if bound <= 1000:
    x_max = 450
    step = 25
    names = [0, 1, 2]
elif bound <= 100000:
    x_max = 5500
    step = 250
    names = [1, 2]
else:
    x_max = 12000000
    step = 1000000
    names = [2]

LABELS = ["slice sums", "running sums", "prefix + min"]
STYLE = [0, 1, 2]
xs = list(range(step, x_max + 1, step))
y_max = max(BUDGET, max(counts(x_max)[i] for i in names)) * 12 // 10
y_max = (y_max // 1000000 + 1) * 1000000
points = {i: [] for i in names}


def frame(x_now):
    series = [(f"s{i}", LABELS[i], list(points[i]), STYLE[i]) for i in names]
    series.append(("budget", "10^7 budget", [(0, BUDGET), (x_max, BUDGET)], 3))
    return vz.plot(
        x=(0, x_max, "n"),
        y=(0, y_max, "additions"),
        series=series,
        vline=(bound, f"N ≤ {bound}" if bound < 100000 else "N ≤ 10^6"),
    )


def words(v):
    return f"{v:,}"


for n in xs:
    c = counts(n)
    for i in names:
        points[i].append((n, c[i]))
    parts = ", ".join(f"{LABELS[i]} {words(c[i])}" for i in names)
    if n == bound:
        parts = "the subtask's bound: " + parts
    over = [LABELS[i] for i in names if c[i] > BUDGET]
    if over:
        tail = f" Over the budget: {', '.join(over)}."
    else:
        tail = " All are under the budget."
    if n == bound:
        tail += f" The plan written for this subtask uses {c[names[0]] / BUDGET:.0%} of the budget."
    rec.step(f"At n = {words(n)}: {parts}.{tail}", plot=frame(n))

c = counts(bound)
rec.output(f"n={bound} cubic={c[0]} quadratic={c[1]} linear={c[2]}\n")
