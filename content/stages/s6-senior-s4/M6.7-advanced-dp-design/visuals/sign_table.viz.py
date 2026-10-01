import vizrec as vz

rec = vz.Recorder()
n, max_signs, gap = (int(x) for x in rec.readline().split())
sites = []
for _ in range(n):
    x, profit = (int(v) for v in rec.readline().split())
    sites.append((x, profit))
sites.sort()
xs = [x for x, _ in sites]

rows = [[""] * n for _ in range(max_signs)]
states = [["_"] * n for _ in range(max_signs)]


def table(arrow=None):
    cells = [list(r) for r in rows]
    return vz.table(
        cells,
        states=["".join(r) for r in states],
        row_heads=[f"{s} sign" if s == 1 else f"{s} signs" for s in range(1, max_signs + 1)],
        col_heads=[str(i) for i in range(n)],
        arrows=[arrow] if arrow else None,
    )


def sites_frame(i=None, p=None):
    st = None
    ptrs = None
    if i is not None:
        st = ["done" if j < p else ("current" if j == i else "none") for j in range(n)]
        ptrs = [("i", i, "above"), ("p", p, "below")]
    return vz.array(xs, states=st, pointers=ptrs, indices=True)


prev = [profit for _, profit in sites]
for i in range(n):
    rows[0][i] = prev[i]
answer = max(prev)
rec.step(
    "With one sign, the best profit at each site is that site's own profit, so row 1 is "
    f"`{prev}`. The sites are sorted by position `x`: {', '.join(map(str, xs))}. "
    f"A gap of {gap} must separate any two signs.",
    a=sites_frame(), t=table(),
)

for signs in range(2, max_signs + 1):
    r = signs - 1
    cur = [0] * n
    best_before = 0
    best_at = -1
    p = 0
    for i in range(n):
        limit = xs[i] - gap
        while xs[p] <= limit:
            if prev[p] > best_before:
                best_before = prev[p]
                best_at = p
            p += 1
        x, profit = sites[i]
        if best_before > 0:
            cur[i] = best_before + profit
            rows[r][i] = cur[i]
            states[r][i] = "c"
            states[r - 1][best_at] = "m"
            rec.step(
                f"Row {signs}, site {i} (x = {x}, profit {profit}). The pointer `p` has folded in "
                f"every site at or left of x - {gap} = {limit}; the best row {signs - 1} cell "
                f"among them is {best_before}, at site {best_at}. So the cell is "
                f"{best_before} + {profit} = {cur[i]}.",
                a=sites_frame(i, p), t=table(((r - 1, best_at), (r, i))),
            )
            states[r - 1][best_at] = "_"
            states[r][i] = "_"
        else:
            rows[r][i] = "-"
            states[r][i] = "x"
            rec.step(
                f"Row {signs}, site {i} (x = {x}). No earlier site with a legal cell sits at or "
                f"left of x - {gap} = {limit}, so there is no way to end here with {signs} signs: "
                "the cell is `-`.",
                a=sites_frame(i, p), t=table(),
            )
            states[r][i] = "x"
    answer = max(answer, max(cur))
    prev = cur

best_cell = None
for r in range(max_signs):
    for c in range(n):
        if rows[r][c] == answer and best_cell is None:
            best_cell = (r, c)
states[best_cell[0]][best_cell[1]] = "p"
rec.step(
    f"Every row is filled. The largest cell is {answer}, in row {best_cell[0] + 1}, site "
    f"{best_cell[1]}. That is the program's answer.",
    a=sites_frame(), t=table(),
)
rec.output(f"{answer}\n")
