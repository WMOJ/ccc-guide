import vizrec as vz

rec = vz.Recorder()
n = int(rec.readline())
piles = list(map(int, rec.readline().split()))

prefix = [0] * (n + 1)
for i in range(n):
    prefix[i + 1] = prefix[i] + piles[i]

dp = [[None] * n for _ in range(n)]
for i in range(n):
    dp[i][i] = 0


def table(cur=None, srcs=(), arrows=None):
    cells = []
    states = []
    for i in range(n):
        crow = []
        srow = []
        for j in range(n):
            if j < i or dp[i][j] is None:
                crow.append(None)
                srow.append("_")
            else:
                crow.append(dp[i][j])
                srow.append("d")
        cells.append(crow)
        states.append(srow)
    for (r, c) in srcs:
        states[r][c] = "m"
    if cur is not None:
        states[cur[0]][cur[1]] = "c"
    return vz.table(cells, states=states, row_heads=list(range(n)), col_heads=list(range(n)),
                    row_title="i", col_title="j", arrows=arrows)


def arr(i=None, j=None, k=None):
    if i is None:
        return vz.array(piles, name="piles", indices=True)
    marks = ["_"] * n
    for x in range(i, k + 1):
        marks[x] = "d"
    for x in range(k + 1, j + 1):
        marks[x] = "m"
    return vz.array(
        piles,
        states=marks,
        ranges=[(i, k, f"left {i}..{k}"), (k + 1, j, f"right {k + 1}..{j}")],
        name="piles",
        indices=True,
    )


rec.step(
    f"Piles {piles}. dp[i][j] is the cheapest way to merge piles i through j into one. A single "
    "pile needs no merge, so the diagonal dp[i][i] is 0. Every longer interval is still empty.",
    arr=arr(), tab=table()
)
for size in range(2, n + 1):
    for i in range(n - size + 1):
        j = i + size - 1
        span = prefix[j + 1] - prefix[i]
        totals = [dp[i][k] + dp[k + 1][j] + span for k in range(i, j)]
        best = min(totals)
        k = i + totals.index(best)
        dp[i][j] = best
        listing = ", ".join(f"k={i + t}: {v}" for t, v in enumerate(totals))
        rec.step(
            f"Length {size}, interval {i}..{j} (range sum {span}). Totals dp[{i}][k] + "
            f"dp[k+1][{j}] + {span}: {listing}. The smallest is {best} at k = {k}, so "
            f"dp[{i}][{j}] = {best}; arrows show the two cells it used.",
            arr=arr(i, j, k),
            tab=table((i, j), [(i, k), (k + 1, j)], [((i, k), (i, j)), ((k + 1, j), (i, j))]),
        )
rec.output(f"Minimum cost: {dp[0][n - 1]}\n")
