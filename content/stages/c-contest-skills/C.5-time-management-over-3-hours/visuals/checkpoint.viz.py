import vizrec as vz

rec = vz.Recorder()
t = rec.stdin.split()
left = int(t[0])
cleared = []
nxt = []
for p in range(1, 6):
    cleared.append(int(t[2 * p - 1]))
    word = t[2 * p]
    nxt.append(None if word == "-" else int(word))

fits = ["?"] * 5
states = ["___"] * 5


def frame(chosen=None):
    cells = []
    sts = []
    for i in range(5):
        cost = "none left" if nxt[i] is None else str(nxt[i])
        cells.append([str(cleared[i]), cost, fits[i]])
        if chosen is not None and i == chosen:
            sts.append("ppp")
        else:
            sts.append(states[i])
    return vz.table(
        cells=cells,
        states=sts,
        row_heads=["P1", "P2", "P3", "P4", "P5"],
        col_heads=["cleared", "next cost", "fits"],
    )


rec.step(
    f"A checkpoint with {left} minutes left. For each problem you write how many subtasks "
    "have cleared and your estimate, in minutes, for the next one. The fits column is still empty.",
    table=frame(),
)
best = None
for i in range(5):
    name = f"Problem {i + 1}"
    if nxt[i] is None:
        fits[i] = "no"
        states[i] = "__x"
        rec.step(f"{name} has no subtask left to try, so it is not a candidate.", table=frame())
        continue
    if nxt[i] > left:
        fits[i] = "no"
        states[i] = "__x"
        rec.step(
            f"{name}: the next subtask is estimated at {nxt[i]} minutes, more than the {left} "
            "left, so it does not fit.",
            table=frame(),
        )
        continue
    fits[i] = "yes"
    states[i] = "__d"
    if best is None or nxt[i] < nxt[best]:
        if best is None:
            why = "It is the first candidate."
        else:
            why = f"That beats problem {best + 1}'s {nxt[best]}, so it becomes the pick."
        best = i
    elif nxt[i] == nxt[best]:
        why = f"It ties with problem {best + 1}'s {nxt[best]}, and the lower-numbered problem stays the pick."
    else:
        why = f"Problem {best + 1}'s {nxt[best]} is smaller, so the pick stays."
    rec.step(f"{name}: the next subtask is estimated at {nxt[i]} minutes and fits. {why}", table=frame())

if best is None:
    rec.step(
        f"No estimate fits in {left} minutes, so there is no next subtask to start. "
        "That is a signal to spend the time on what you already have.",
        table=frame(),
    )
    rec.output(f"nothing fits in {left} minutes\n")
else:
    rec.step(
        f"Pick problem {best + 1}: its next subtask has the smallest estimate that fits, "
        f"{nxt[best]} minutes.",
        table=frame(best),
    )
    rec.output(f"pick problem {best + 1} for {nxt[best]} minutes\n")
