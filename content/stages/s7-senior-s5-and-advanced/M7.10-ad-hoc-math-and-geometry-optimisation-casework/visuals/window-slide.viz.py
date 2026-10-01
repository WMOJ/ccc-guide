import vizrec as vz

rec = vz.Recorder()
data = rec.stdin.split()
n = int(data[0])
k = int(data[1])
grid = [[int(data[2 + r * n + c]) for c in range(n)] for r in range(n)]
prefix = [[0] * (n + 1) for _ in range(n + 1)]
for r in range(1, n + 1):
    for c in range(1, n + 1):
        prefix[r][c] = grid[r - 1][c - 1] + prefix[r - 1][c] + prefix[r][c - 1] - prefix[r - 1][c - 1]


def neg(v):
    return f"({v})" if v < 0 else str(v)


def cells(window=None, best=None):
    rows = []
    for r in range(n):
        row = ""
        for c in range(n):
            if window and window[0] <= r < window[0] + k and window[1] <= c < window[1] + k:
                row += "c"
            elif best and best[0] <= r < best[0] + k and best[1] <= c < best[1] + k:
                row += "d"
            else:
                row += "."
        rows.append(row)
    return vz.grid(rows, values=grid)


rec.step(
    f"A {n} by {n} grid and a {k} by {k} window. The prefix table P, built once as in M4.3, lets "
    "each window's sum come from four reads. The window visits every position, top-left corner "
    "by top-left corner.",
    g=cells(),
)
best = None
best_at = None
for r in range(n - k + 1):
    for c in range(n - k + 1):
        a = prefix[r + k][c + k]
        b = prefix[r][c + k]
        d = prefix[r + k][c]
        e = prefix[r][c]
        total = a - b - d + e
        if best is None or total > best:
            best, best_at = total, (r, c)
            verdict = f"New best, {neg(total)}."
        else:
            verdict = f"Best stays {neg(best)}."
        rec.step(
            f"Window at row {r}, column {c}: {neg(a)} - {neg(b)} - {neg(d)} + {neg(e)} = {neg(total)}. {verdict}",
            g=cells(window=(r, c), best=best_at if best_at != (r, c) else None),
        )
count = (n - k + 1) ** 2
rec.step(
    (f"Every one of the {count} windows is checked. " if count > 1 else "The window fits in one place only. ")
    + f"The best sum is {best}, with the window's top-left corner at row {best_at[0]}, column {best_at[1]}.",
    g=cells(best=best_at),
)
rec.output(f"{best}\n{best_at[0]} {best_at[1]}\n")
