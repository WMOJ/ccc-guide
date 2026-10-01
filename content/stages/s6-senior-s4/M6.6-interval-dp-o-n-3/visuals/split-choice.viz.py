import vizrec as vz

rec = vz.Recorder()
n = int(rec.readline())
piles = list(map(int, rec.readline().split()))

prefix = [0] * (n + 1)
for i in range(n):
    prefix[i + 1] = prefix[i] + piles[i]

dp = [[0] * n for _ in range(n)]
for size in range(2, n + 1):
    for i in range(n - size + 1):
        j = i + size - 1
        best = min(dp[i][k] + dp[k + 1][j] for k in range(i, j))
        dp[i][j] = best + prefix[j + 1] - prefix[i]

total = prefix[n]
rows = []
states = []


def table():
    cells = [list(r) for r in rows]
    st = [list(s) for s in states]
    while len(cells) < n - 1:
        cells.append(["", "", ""])
        st.append(["_", "_", "_"])
    return vz.table(
        cells,
        states=st,
        row_heads=[f"k={k}" for k in range(n - 1)],
        col_heads=["dp left", "dp right", "total"],
    )


def arr(k=None, best=False):
    if k is None:
        return vz.array(piles, name="piles", indices=True)
    marks = ["d"] * (k + 1) + ["m"] * (n - k - 1)
    return vz.array(
        piles,
        states=marks,
        ranges=[(0, k, f"left 0..{k}"), (k + 1, n - 1, f"right {k + 1}..{n - 1}")],
        name="piles",
        indices=True,
    )


rec.step(
    f"Piles {piles}, total {total}. The last merge joins a left block and a right block, and "
    f"always costs the whole range sum, {total}. Which split k is best depends only on the "
    "two blocks' own costs, dp left and dp right.",
    arr=arr(), tab=table()
)
cands = []
for k in range(n - 1):
    left = dp[0][k]
    right = dp[k + 1][n - 1]
    cands.append(left + right + total)
    rows.append([left, right, left + right + total])
    states.append(["c", "c", "c"])
    rec.step(
        f"k = {k}: the left block is piles 0..{k} with dp[0][{k}] = {left}, the right block is "
        f"piles {k + 1}..{n - 1} with dp[{k + 1}][{n - 1}] = {right}. Total {left} + {right} + "
        f"{total} = {left + right + total}.",
        arr=arr(k), tab=table()
    )
    states[-1] = ["d", "d", "d"]
best_total = min(cands)
best_k = cands.index(best_total)
states[best_k] = ["p", "p", "p"]
rec.step(
    f"The smallest total is {best_total}, at k = {best_k}. That is dp[0][{n - 1}], the "
    "minimum cost of merging all the piles.",
    arr=arr(best_k), tab=table()
)
rec.output(f"Minimum cost: {dp[0][n - 1]}\n")
