import vizrec as vz

rec = vz.Recorder()
n = int(rec.readline())

freq_pts = []
count_pts = []


def frame():
    y_max = max(n, 26 * n, 1)
    return vz.plot(
        x=(0, max(n, 1) + (1 if n <= 1 else 0), "word length n"),
        y=(0, y_max, "character comparisons"),
        series=[
            ("freq", "freq array", list(freq_pts), 0),
            ("count", "count() x26", list(count_pts), 1),
        ],
    )


for k in range(1, n + 1):
    freq_ops = k
    count_ops = 26 * k
    freq_pts.append((k, freq_ops))
    count_pts.append((k, count_ops))
    freq_word = "operation" if freq_ops == 1 else "operations"
    rec.step(
        f"At n = {k}: the frequency array does {freq_ops} {freq_word} in one pass. "
        f"Calling .count() for each of the 26 letters scans the word 26 times over, "
        f"{count_ops} comparisons in total.",
        plot=frame(),
    )

rec.output(f"{n} {26 * n}\n")
