import vizrec as vz

rec = vz.Recorder()
top = int(rec.readline())


def brute(w):
    best_x, best_area = 0, 0
    for x in range(1, (w - 1) // 2 + 1):
        if x * (w - 2 * x) > best_area:
            best_x, best_area = x, x * (w - 2 * x)
    return best_x, best_area


def short(w, picks):
    hi = (w - 1) // 2
    best_x, best_area = 0, 0
    for pick in picks:
        x = max(1, min(hi, pick))
        if x * (w - 2 * x) > best_area:
            best_x, best_area = x, x * (w - 2 * x)
    return best_x, best_area


first_miss = None
both_misses = 0
for w in range(3, top + 1):
    want = brute(w)
    if short(w, [w // 4]) != want and first_miss is None:
        first_miss = w
    if short(w, [w // 4, w // 4 + 1]) != want:
        both_misses += 1

ws = list(range(max(3, top - 5), top + 1))
rows = [[brute(w)[0] for w in ws], [short(w, [w // 4])[0] for w in ws], [short(w, [w // 4, w // 4 + 1])[0] for w in ws]]


def table(upto):
    cells = []
    states = []
    for r in range(3):
        cells.append([rows[r][i] if i < upto else "" for i in range(len(ws))])
        states.append("".join(
            "_" if i >= upto or r == 0 else ("d" if rows[r][i] == rows[0][i] else "x")
            for i in range(len(ws))
        ))
    return vz.table(cells, states=states, row_heads=["brute", "floor", "floor+1"], col_heads=ws, col_title="W")


rec.step(
    "Row floor tries only W/4 rounded down. Row floor+1 also tries the next whole number. "
    "Before trusting either, compare with brute force for each wire length W. Each cell is the "
    "best side length x.",
    t=table(0),
)
for i, w in enumerate(ws):
    b = brute(w)[0]
    f = short(w, [w // 4])[0]
    g = short(w, [w // 4, w // 4 + 1])[0]
    if f == b:
        note = f"The floor alone also finds x = {b}."
    else:
        note = f"The floor alone picks x = {f}, but the best is x = {b}: a miss."
    rec.step(
        f"W = {w}: brute force finds x = {b}. Floor and the next whole number find x = {g}. {note}",
        t=table(i + 1),
    )
if first_miss is None:
    tail = "The floor alone was never wrong up to the limit."
else:
    tail = f"The floor alone first fails at W = {first_miss}."
rec.step(
    f"{tail} Floor and the next whole number were wrong {both_misses} times up to W = {top}.",
    t=table(len(ws)),
)
rec.output(
    ("floor only: no wrong answer\n" if first_miss is None else f"floor only: first wrong at {first_miss}\n")
    + f"floor and next: wrong {both_misses} times\n"
)
