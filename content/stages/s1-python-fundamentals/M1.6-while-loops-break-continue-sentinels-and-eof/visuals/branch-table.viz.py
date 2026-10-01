import vizrec as vz

rec = vz.Recorder()
numbers = [int(line) for line in rec.stdin.split()]

rows = []
total = 0


def frame(last_state):
    states = []
    for i in range(len(rows)):
        states.append("ddd" if i < len(rows) - 1 else last_state)
    return vz.table(rows, states=states, col_heads=["n", "branch", "total"])


for n in numbers:
    if n == 0:
        rows.append([n, "break", total])
        rec.step(
            f"`n` is 0, so `break` leaves the loop at once. Nothing below it runs, and total stays {total}.",
            t=frame("xxx"),
        )
        break
    if n < 0:
        rows.append([n, "continue", total])
        rec.step(
            f"`n` is {n}, which is negative. `continue` jumps back to the top of the loop and skips `total += n`, so total stays {total}.",
            t=frame("ccc"),
        )
        continue
    total += n
    rows.append([n, "add", total])
    rec.step(
        f"`n` is {n}: not 0 and not negative, so `total += n` runs and total becomes {total}.",
        t=frame("ccc"),
    )

rec.step(
    f"The loop is over, so `print(total)` shows {total}.",
    t=frame("xxx"),
)
rec.output(f"{total}\n")
