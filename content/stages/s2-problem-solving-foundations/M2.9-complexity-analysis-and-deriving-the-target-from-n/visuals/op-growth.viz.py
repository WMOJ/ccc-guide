import vizrec as vz

rec = vz.Recorder()
n = int(rec.readline())

y_max = max(n, n * (n - 1) // 2, 1)
single_pts = []
nested_pts = []


def frame():
    return vz.plot(
        x=(0, max(n, 1) + (1 if n <= 1 else 0), "n"),
        y=(0, y_max, "total operations"),
        series=[
            ("single", "single loop", list(single_pts), 0),
            ("nested", "nested loop", list(nested_pts), 1),
        ],
    )


for k in range(1, n + 1):
    single_total = k
    nested_total = k * (k - 1) // 2
    single_pts.append((k, single_total))
    nested_pts.append((k, nested_total))
    single_word = "operation" if single_total == 1 else "operations"
    nested_word = "operation" if nested_total == 1 else "operations"
    rec.step(
        f"At n = {k}: the single loop does {single_total} {single_word}, "
        f"the nested loop does {nested_total} {nested_word}.",
        plot=frame(),
    )

nested_final = n * (n - 1) // 2
rec.output(f"{nested_final}\n")
