import vizrec as vz

rec = vz.Recorder()
data = rec.stdin.split()
idx = 0
n = int(data[idx])
idx += 1
items = []
for _ in range(n):
    name = data[idx]
    duration = int(data[idx + 1])
    items.append((name, duration))
    idx += 2


def table_frame(order, highlight=None):
    names = [t[0] for t in order]
    keys = [t[1] for t in order]
    width = len(order)
    key_states = ["_"] * width
    if highlight is not None:
        key_states[highlight] = "c"
    return vz.table(
        [names, keys],
        states=["_" * width, "".join(key_states)],
        row_heads=["item", "key"],
        col_heads=list(range(width)),
        col_title="position",
    )


rec.step(
    "Each task's key is its duration, read off in the order the input lists them.",
    table=table_frame(items),
)

for i in range(n):
    rec.step(
        f"Position {i} holds \"{items[i][0]}\", key {items[i][1]}.",
        table=table_frame(items, highlight=i),
    )

ordered = sorted(items, key=lambda task: task[1])
if ordered != items:
    rec.step(
        "sorted() rearranges the tasks by key, ascending: the shortest duration goes first.",
        table=table_frame(ordered),
    )
    tied = [t for t in items if any(o[1] == t[1] and o[0] != t[0] for o in items)]
    if tied:
        names = ", ".join(t[0] for t in tied)
        rec.step(
            f"{names} share a duration. Python's sort is stable, so they keep their original "
            "relative order instead of swapping places.",
            table=table_frame(ordered),
        )
else:
    rec.step(
        "The tasks were already in duration order, so sorted() leaves the arrangement unchanged.",
        table=table_frame(ordered),
    )

lines = [f"{name} {duration}" for name, duration in ordered]
rec.output("\n".join(lines) + "\n")
