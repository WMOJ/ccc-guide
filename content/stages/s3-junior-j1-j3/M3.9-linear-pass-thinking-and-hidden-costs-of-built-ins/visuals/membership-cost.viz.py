import vizrec as vz

rec = vz.Recorder()
n = int(rec.readline())

list_pts = []
set_pts = []


def frame():
    y_max = max(n * (n - 1) // 2, n, 1)
    return vz.plot(
        x=(0, max(n, 1) + (1 if n <= 1 else 0), "numbers read so far"),
        y=(0, y_max, "membership checks"),
        series=[
            ("list", "list in-check", list(list_pts), 0),
            ("set", "set in-check", list(set_pts), 1),
        ],
    )


for k in range(1, n + 1):
    list_ops = k * (k - 1) // 2
    set_ops = k
    list_pts.append((k, list_ops))
    set_pts.append((k, set_ops))
    rec.step(
        f"After reading {k} distinct numbers: checking against a growing list has cost "
        f"{list_ops} comparisons in total, since each check scans everything read so far. "
        f"Checking against a set has cost {set_ops}, one hash lookup per number.",
        plot=frame(),
    )

list_final = n * (n - 1) // 2
rec.output(f"{list_final} {n}\n")
