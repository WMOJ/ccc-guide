import vizrec as vz

rec = vz.Recorder()
data = rec.stdin.split()
idx = 0
n = int(data[idx])
capacity = int(data[idx + 1])
idx += 2
boxes = []
for _ in range(n):
    weight = int(data[idx])
    value = int(data[idx + 1])
    boxes.append((weight, value))
    idx += 2

labels = [chr(ord("A") + i) for i in range(n)]


def table_frame(states_row=None):
    weights = [b[0] for b in boxes]
    values = [b[1] for b in boxes]
    states = [states_row, states_row] if states_row else None
    return vz.table([weights, values], states=states, row_heads=["weight", "value"], col_heads=labels)


rec.step(
    f"Three boxes, capacity {capacity}. Ratio, value over weight, ranks {labels[0]} first among "
    f"them.",
    table=table_frame(),
)

order = sorted(range(n), key=lambda i: boxes[i][1] / boxes[i][0], reverse=True)
greedy_weight = 0
greedy_value = 0
taken = []
row = "_" * n
for i in order:
    weight, value = boxes[i]
    if greedy_weight + weight <= capacity:
        greedy_weight += weight
        greedy_value += value
        taken.append(i)
        row = "".join("d" if j in taken else "_" for j in range(n))
        rec.step(
            f"Ratio order takes {labels[i]} (weight {weight}): {greedy_weight - weight} + "
            f"{weight} = {greedy_weight} <= {capacity}. Value so far: {greedy_value}.",
            table=table_frame(row),
        )
    else:
        rec.step(
            f"Ratio order reaches {labels[i]} (weight {weight}), but {greedy_weight} + "
            f"{weight} = {greedy_weight + weight} would exceed {capacity}. Skip it.",
            table=table_frame(row),
        )

rec.step(
    f"Ratio-greedy's final load: {', '.join(labels[i] for i in taken)}, total value "
    f"{greedy_value}.",
    table=table_frame(row),
)

best_value = 0
best_subset = tuple(taken)
for mask in range(1 << n):
    weight = 0
    value = 0
    subset = []
    for i in range(n):
        if mask & (1 << i):
            weight += boxes[i][0]
            value += boxes[i][1]
            subset.append(i)
    if weight <= capacity and value > best_value:
        best_value = value
        best_subset = tuple(subset)

best_row = "".join("m" if j in best_subset else "_" for j in range(n))
if best_value > greedy_value:
    rec.step(
        f"But {' and '.join(labels[i] for i in best_subset)} together weigh "
        f"{sum(boxes[i][0] for i in best_subset)} and are worth {best_value}, more than "
        f"ratio-greedy found. Taking whole boxes by ratio is a heuristic, not a proof.",
        table=table_frame(best_row),
    )
else:
    rec.step(
        f"No other combination that fits is worth more than {best_value}: here, ratio order "
        "happens to find the best load too.",
        table=table_frame(best_row),
    )

rec.output(f"{greedy_value}\n{best_value}\n")
