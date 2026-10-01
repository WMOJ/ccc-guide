import vizrec as vz

rec = vz.Recorder()
data = rec.stdin.split()
idx = 0
n = int(data[idx])
capacity = int(data[idx + 1])
idx += 2
weights = [int(data[idx + i]) for i in range(n)]
idx += n

rec.step(
    f"Each box has a weight. The truck's capacity is {capacity}, and the goal is to fit as many "
    "boxes as possible.",
    boxes=vz.array(weights),
)

order = sorted(weights)
rec.step(
    "Sorting the boxes by weight, ascending, puts the lightest ones first.",
    boxes=vz.array(order),
)

total_weight = 0
count = 0
states = ["none"] * n
for i, weight in enumerate(order):
    fits = total_weight + weight <= capacity
    states[i] = "current"
    if fits:
        total_weight += weight
        count += 1
        states[i] = "done"
        unit = "box" if count == 1 else "boxes"
        rec.step(
            f"Weight {weight} still fits: {total_weight - weight} + {weight} = {total_weight} "
            f"<= {capacity}. Take it: {count} {unit} loaded so far.",
            boxes=vz.array(order, states=states),
        )
    else:
        states[i] = "invalid"
        rec.step(
            f"Weight {weight} would push the load to {total_weight + weight}, over the capacity "
            f"{capacity}. Skip it; the count stays {count}.",
            boxes=vz.array(order, states=states),
        )

rec.step(
    f"Every box has been considered. Final count: {count} boxes, using {total_weight} of "
    f"{capacity} capacity.",
    boxes=vz.array(order, states=states),
)

rec.output(f"{count}\n")
