import vizrec as vz

rec = vz.Recorder()
n = int(rec.readline())
piles = list(map(int, rec.readline().split()))

prefix = [0] * (n + 1)
for i in range(n):
    prefix[i + 1] = prefix[i] + piles[i]

INF = 10**18
dp = [[0] * n for _ in range(n)]
opt = [[None] * n for _ in range(n)]
for i in range(n):
    opt[i][i] = i


def table(cur=None, srcs=(), arrows=None):
    cells = []
    states = []
    for i in range(n):
        crow = []
        srow = []
        for j in range(n):
            if j < i or opt[i][j] is None:
                crow.append(None)
                srow.append("_")
            else:
                crow.append(opt[i][j])
                srow.append("d")
        cells.append(crow)
        states.append(srow)
    for (r, c) in srcs:
        states[r][c] = "m"
    if cur is not None:
        states[cur[0]][cur[1]] = "c"
    return vz.table(cells, states=states, row_heads=list(range(n)), col_heads=list(range(n)),
                    row_title="i", col_title="j", arrows=arrows)


rec.step(
    f"Piles {piles}. Besides dp, keep opt[i][j], the best split k for interval i..j. For a single "
    "pile opt[i][i] = i. Knuth's rule: the best split of i..j lies between opt[i][j-1] and "
    "opt[i+1][j], so only that window of k values is tried.",
    tab=table()
)
tried = 0
for size in range(2, n + 1):
    for i in range(n - size + 1):
        j = i + size - 1
        low = opt[i][j - 1]
        high = min(opt[i + 1][j], j - 1)
        best = INF
        best_k = low
        for k in range(low, high + 1):
            tried += 1
            cost = dp[i][k] + dp[k + 1][j]
            if cost < best:
                best = cost
                best_k = k
        dp[i][j] = best + prefix[j + 1] - prefix[i]
        opt[i][j] = best_k
        count = high - low + 1
        if size == 2:
            if i == n - 2:
                rec.skip(
                    "Every length-2 interval has just one split, so opt[i][i+1] = i for each "
                    f"of the {n - 1} such intervals; this table holds them all.",
                    n - 1,
                    tab=table(),
                )
            continue
        rec.step(
            f"Interval {i}..{j}: opt[{i}][{j - 1}] = {low} and opt[{i + 1}][{j}] = "
            f"{opt[i + 1][j]}, so k runs from {low} to {high}: {count} of the {size - 1} "
            f"possible splits. The best is k = {best_k}, so opt[{i}][{j}] = {best_k}.",
            tab=table((i, j), [(i, j - 1), (i + 1, j)],
                      [((i, j - 1), (i, j)), ((i + 1, j), (i, j))]),
        )
rec.step(
    f"The table is full. The minimum cost of merging all {n} piles is {dp[0][n - 1]}. The Knuth "
    f"windows tried {tried} splits in all, where the plain loop tries {(n**3 - n) // 6}.",
    tab=table()
)
rec.output(
    f"Minimum cost: {dp[0][n - 1]}\nSplits tried: {tried}\n"
    f"Splits in the plain loop: {(n**3 - n) // 6}\n"
)
