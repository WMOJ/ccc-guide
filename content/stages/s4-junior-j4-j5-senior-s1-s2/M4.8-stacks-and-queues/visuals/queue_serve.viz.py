import vizrec as vz

rec = vz.Recorder()
orders = rec.stdin.split()

remaining = list(orders)
served = []

rec.step(
    f"{len(orders)} {'order waits' if len(orders) == 1 else 'orders wait'} in line with "
    f"'{orders[0]}' at the front. Nothing has been served yet.",
    queue=vz.queue(remaining),
    served=vz.array(["-"], states=["none"], name="Served"),
)
while remaining:
    order = remaining.pop(0)
    served.append(order)
    left = len(remaining)
    if left:
        tail = f"{left} {'order remains' if left == 1 else 'orders remain'} and '{remaining[0]}' is now at the front."
    else:
        tail = "The line is empty."
    rec.step(
        f"'{order}' was at the front and is served next. {tail}",
        queue=vz.queue(remaining) if remaining else vz.queue([("empty", "none")]),
        served=vz.array(served, states=["done"] * len(served), name="Served"),
    )

rec.output("\n".join(f"Served: {o}" for o in served) + "\n")
