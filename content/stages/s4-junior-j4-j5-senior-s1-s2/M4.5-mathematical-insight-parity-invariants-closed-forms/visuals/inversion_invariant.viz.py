import vizrec as vz


def count_inversions(values):
    total = 0
    for i in range(len(values)):
        for j in range(i + 1, len(values)):
            if values[i] > values[j]:
                total += 1
    return total


def frame(values, swaps, compare=None):
    inv = count_inversions(values)
    arr_states = None
    if compare is not None:
        arr_states = {compare[0]: "compare", compare[1]: "compare"}
    return {
        "arr": vz.array(values, states=arr_states),
        "counts": vz.table(
            cells=[[inv, swaps]],
            row_heads=["so far"],
            col_heads=["inversions", "swaps"],
        ),
    }


rec = vz.Recorder()
data = rec.stdin.split()
n = int(data[0])
values = list(map(int, data[1:1 + n]))

swaps = 0
initial_inversions = count_inversions(values)
step_frame = frame(values, swaps)
rec.step(
    f"Start with {values}. It has {initial_inversions} inversions: pairs where an earlier "
    "value is bigger than a later one.",
    **step_frame,
)

changed = True
while changed:
    changed = False
    for i in range(n - 1):
        if values[i] > values[i + 1]:
            before = count_inversions(values)
            left, right = values[i], values[i + 1]
            values[i], values[i + 1] = right, left
            swaps += 1
            after = count_inversions(values)
            rec.step(
                f"Swap positions {i} and {i + 1} ({left} then {right}, out of order): the count drops "
                f"from {before} to {after}. Every swap here fixes exactly one inversion.",
                **frame(values, swaps, compare=(i, i + 1)),
            )
            changed = True

rec.step(
    f"No adjacent pair is out of order: {count_inversions(values)} inversions left, so the array "
    f"is sorted after exactly {swaps} swaps, the number it started with.",
    **frame(values, swaps),
)

lines = []
lines.append(str(initial_inversions))
lines.append(str(swaps))
lines.append(" ".join(str(v) for v in values))
rec.output("\n".join(lines) + "\n")
