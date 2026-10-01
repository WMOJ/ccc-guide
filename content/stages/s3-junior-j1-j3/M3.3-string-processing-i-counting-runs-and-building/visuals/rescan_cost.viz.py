import vizrec as vz

rec = vz.Recorder()
s = rec.readline()
n = len(s)


def compares(i):
    """Comparisons the inner loop makes for a run scan that starts at index i."""
    k = 1
    total = 0
    while i + k < n:
        total += 1
        if s[i + k] != s[i]:
            break
        k += 1
    return total, k


def word(count):
    return f"{count} comparison{'s' if count != 1 else ''}"


slow_pts = [(0, 0)]
fast_pts = []
slow_total = 0
for i in range(n):
    made, _ = compares(i)
    slow_total += made
    slow_pts.append((i + 1, slow_total))

fast_total = 0
fast_run = [(0, 0)]
i = 0
while i < n:
    made, k = compares(i)
    fast_total += made
    i += k
    fast_run.append((i, fast_total))

y_max = max(slow_total, fast_total, 1)


def frame(slow, fast, markers=None):
    series = [("slow", "i += 1", list(slow), 0)]
    if fast:
        series.append(("fast", "i += count", list(fast), 1))
    return vz.plot(
        x=(0, n, "index i reached"),
        y=(0, y_max, "comparisons"),
        series=series,
        markers=markers,
    )


running = [(0, 0)]
for i in range(n):
    made, _ = compares(i)
    running.append(slow_pts[i + 1])
    rec.step(
        f"With i += 1, the scan from index {i} makes {word(made)}, so {word(slow_pts[i + 1][1])} in total so far.",
        cost=frame(running, None),
    )

fast_shown = [(0, 0)]
i = 0
for x, y in fast_run[1:]:
    fast_shown.append((x, y))
    before = fast_shown[-2]
    rec.step(
        f"With i += count, one scan from index {before[0]} takes {word(y - before[1])} and i jumps to {x}. "
        f"The running total is {word(y)}.",
        cost=frame(slow_pts, fast_shown),
    )

rec.step(
    f"Final totals on this string: {slow_total} for i += 1 against {fast_total} for i += count."
    + (" With no repeated characters, nothing is rescanned, so the plans tie." if slow_total == fast_total else ""),
    cost=frame(
        slow_pts,
        fast_shown,
        markers=[(n, slow_total, "i += 1", "m"), (n, fast_total, "jump", "d")],
    ),
)

rec.output(f"{slow_total} {fast_total}\n")
