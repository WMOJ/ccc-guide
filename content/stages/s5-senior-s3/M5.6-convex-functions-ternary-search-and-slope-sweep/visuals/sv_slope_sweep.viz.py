import vizrec as vz

rec = vz.Recorder()
n = int(rec.readline())
positions = [int(x) for x in rec.readline().split()]
weights = [int(x) for x in rec.readline().split()]

breakpoints = sorted(zip(positions, weights))
total_weight = sum(weights)
lo, hi = breakpoints[0][0], breakpoints[-1][0]
if lo == hi:
    lo -= 5
    hi += 5


def frame(current=None, found=None):
    pts = []
    for p, w in breakpoints:
        if found is not None and p == found:
            state = "p"
        elif current is not None and p == current:
            state = "c"
        elif current is not None and p < current:
            state = "d"
        else:
            state = "."
        pts.append((p, f"w={w}", state))
    sweep = (current, f"c = {current}") if current is not None else None
    return {"line": vz.line(lo, hi, tick=max(1, (hi - lo) // 10 or 1), points=pts, sweep=sweep)}


rec.step(
    f"Sort the {n} job sites by position. Before sweeping, the slope is `-{total_weight}`: moving "
    f"c right only helps, since every site still sits to its right.",
    **frame(),
)

left_weight = 0
best_loc = breakpoints[-1][0]
found = False
for p, w in breakpoints:
    left_weight += w
    slope = 2 * left_weight - total_weight
    if not found and slope >= 0:
        best_loc = p
        found = True
        rec.step(
            f"At c = {p}, weight {w} on the left brings the running left weight to {left_weight}. "
            f"The slope is `2*{left_weight} - {total_weight}` = `{slope}`, no longer negative: "
            f"this is the breakpoint where the cost stops falling.",
            **frame(current=p, found=p),
        )
    else:
        rec.step(
            f"At c = {p}, weight {w} on the left brings the running left weight to {left_weight}. "
            f"The slope is `2*{left_weight} - {total_weight}` = `{slope}`"
            + (", still negative: the cost keeps falling past here." if slope < 0
               else ", already found: this later site does not change the answer."),
            **frame(current=p, found=best_loc if found else None),
        )

best_cost = sum(w * abs(p - best_loc) for p, w in zip(positions, weights))
rec.step(
    f"The slope crosses zero at c = {best_loc}: the minimum. Total cost there is {best_cost}.",
    **frame(current=breakpoints[-1][0], found=best_loc),
)

rec.output(f"{best_loc} {best_cost}\n")
