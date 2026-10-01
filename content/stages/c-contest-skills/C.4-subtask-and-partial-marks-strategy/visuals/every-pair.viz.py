import vizrec as vz

rec = vz.Recorder()
n = int(rec.readline())
values = [int(t) for t in rec.readline().split()]

best = values[0]
best_at = (0, 0)
count = 0


def frame(i, j):
    states = ["none"] * n
    for k in range(best_at[0], best_at[1] + 1):
        states[k] = "done"
    for k in range(i, j + 1):
        states[k] = "current"
    total = sum(values[i:j + 1])
    ranges = [(i, j, f"sum {total}")]
    return vz.array(values, states=states, ranges=ranges, index_base=0)


for i in range(n):
    for j in range(i, n):
        count += 1
        total = sum(values[i:j + 1])
        if count == 1:
            text = (
                f"Pair 1 is i = 0, j = 0: the slice values[0:1] sums to {total}. Nothing is larger "
                f"yet, so best starts at {total}."
            )
        elif total > best:
            best = total
            best_at = (i, j)
            text = (
                f"Pair {count} is i = {i}, j = {j}: the slice values[{i}:{j + 1}] sums to {total}. "
                f"That beats the old best, so best becomes {total}."
            )
        else:
            text = (
                f"Pair {count} is i = {i}, j = {j}: the slice values[{i}:{j + 1}] sums to {total}. "
                f"That does not beat best, which stays {best}."
            )
        rec.step(text, values=frame(i, j))

pairs = n * (n + 1) // 2
states = ["none"] * n
for k in range(best_at[0], best_at[1] + 1):
    states[k] = "done"
rec.step(
    f"All {pairs} {'pair is' if pairs == 1 else 'pairs are'} checked. The largest sum is {best}, "
    f"from values[{best_at[0]}:{best_at[1] + 1}], which is what every_pair.py prints.",
    values=vz.array(
        values,
        states=states,
        ranges=[(best_at[0], best_at[1], f"best {best}")],
        index_base=0,
    ),
)
rec.output(f"{best}\n")
