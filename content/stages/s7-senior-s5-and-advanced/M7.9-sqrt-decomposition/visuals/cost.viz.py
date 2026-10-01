import vizrec as vz

rec = vz.Recorder()
n = int(rec.readline())


def worst(b):
    """Largest single-value count, largest whole-block count and largest total over all ranges."""
    edges = 0
    whole = 0
    both = 0
    for lo0 in range(n):
        for hi in range(lo0 + 1, n + 1):
            lo = lo0
            e = 0
            w = 0
            while lo < hi and lo % b != 0:
                e += 1
                lo += 1
            while lo + b <= hi:
                w += 1
                lo += b
            while lo < hi:
                e += 1
                lo += 1
            edges = max(edges, e)
            whole = max(whole, w)
            both = max(both, e + w)
    return edges, whole, both


rows = [worst(b) for b in range(1, n + 1)]
xs = list(range(1, n + 1))
best = min(range(n), key=lambda i: (rows[i][2], i))
top = max(r[2] for r in rows)
ticks = [1, n // 4, n // 2, n]


def frame(show, marker=False):
    series = []
    if show >= 1:
        series.append(("e", "single values", [(xs[i], rows[i][0]) for i in range(n)], 0))
    if show >= 2:
        series.append(("w", "whole blocks", [(xs[i], rows[i][1]) for i in range(n)], 1))
    if show >= 3:
        series.append(("t", "total", [(xs[i], rows[i][2]) for i in range(n)], 2))
    mk = [(xs[best], rows[best][2], f"b={xs[best]}", "c")] if marker else None
    return vz.plot(
        x=(1, n, "block size b", ticks),
        y=(0, top, "worst-case additions"),
        series=series,
        markers=mk,
    )


rec.step(
    f"For {n} values, take every possible range and count the additions a query makes. Single "
    f"values on the two ragged edges: none at b = 1, where every block is one value, and "
    f"up to {rows[n - 1][0]} at b = {n}.",
    plot=frame(1)
)
rec.step(
    f"Whole blocks work the other way. At b = 1 a query can add {rows[0][1]} blocks, one per "
    f"value, and with b = {n} at most {rows[n - 1][1]}. More blocks fit when blocks are small.",
    plot=frame(2)
)
rec.step(
    f"The total is the largest count of additions in one query. It falls, then rises. The "
    f"lowest point is b = {xs[best]} with {rows[best][2]} additions, against {rows[0][2]} at "
    f"b = 1 and {rows[n - 1][2]} at b = {n}.",
    plot=frame(3, marker=True)
)
rec.output(f"{n} {xs[best]} {rows[best][2]}\nb=1: {rows[0][2]} b=n: {rows[n - 1][2]}\n")
