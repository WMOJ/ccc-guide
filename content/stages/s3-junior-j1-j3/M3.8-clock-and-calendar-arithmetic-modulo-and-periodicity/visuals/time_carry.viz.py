import vizrec as vz

rec = vz.Recorder()
hour = int(rec.readline())
minute = int(rec.readline())
added = int(rec.readline())

total = hour * 60 + minute + added
hours_total, minutes = divmod(total, 60)
days, hours = divmod(hours_total, 24)

heads = ["minutes", "hours", "days"]
cols = ["total", "size", "carry", "keep"]


def frame(rows, states=None):
    return vz.table(rows, states=states, row_heads=heads, col_heads=cols)


blank = "?"
rows = [[total, 60, blank, blank], [blank, 24, blank, blank], [blank, "-", "-", blank]]
rec.step(
    f"Start at {hour}:{minute} and add {added} minutes. Everything becomes minutes first: "
    f"{hour} * 60 + {minute} + {added} = {total}.",
    table=frame(rows, {(0, 0): "current"}),
)

rows = [[total, 60, hours_total, minutes], [blank, 24, blank, blank], [blank, "-", "-", blank]]
rec.step(
    f"divmod({total}, 60) gives {hours_total} and {minutes}: {minutes} minutes stay on the clock, "
    f"and {hours_total} hours carry over to the next row.",
    table=frame(rows, {(0, 2): "done", (0, 3): "path"}),
)

rows = [
    [total, 60, hours_total, minutes],
    [hours_total, 24, days, hours],
    [blank, "-", "-", days],
]
rec.step(
    f"divmod({hours_total}, 24) gives {days} and {hours}: {hours} hours stay on the clock, "
    f"and {days} {'day carries' if days == 1 else 'days carry'} over.",
    table=frame(rows, {(1, 0): "current", (1, 2): "done", (1, 3): "path"}),
)

rows = [
    [total, 60, hours_total, minutes],
    [hours_total, 24, days, hours],
    [days, "-", "-", days],
]
rec.step(
    f"Nothing is left to carry. The answer is {days} {'day' if days == 1 else 'days'} later, "
    f"hour {hours}, minute {minutes}.",
    table=frame(rows, {(0, 3): "path", (1, 3): "path", (2, 3): "path"}),
)
rec.output(f"{days} {hours} {minutes}\n")
