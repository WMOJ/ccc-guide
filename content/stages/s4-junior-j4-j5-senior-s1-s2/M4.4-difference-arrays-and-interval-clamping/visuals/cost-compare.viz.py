import vizrec as vz

rec = vz.Recorder()
data = rec.stdin.split()
idx = 0
n = int(data[idx])
m = int(data[idx + 1])
idx += 2
updates = []
for _ in range(m):
    l, r, val = int(data[idx]), int(data[idx + 1]), int(data[idx + 2])
    updates.append((l, r, val))
    idx += 3

direct = [0] * n
diff = [0] * (n + 1)


def direct_frame(lo=None, hi=None):
    states = ["none"] * n
    if lo is not None:
        for i in range(lo, hi + 1):
            states[i] = "current"
    return vz.array(direct, states=states)


def diff_frame(marks=None):
    states = ["none"] * (n + 1)
    for i in marks or []:
        states[i] = "current"
    return vz.array(diff, states=states, index_base=0)


rec.step(
    f"Both methods start from {n} zeros and face the same {m} updates. The direct loop writes "
    "every index in each range. The difference array writes two entries per update.",
    direct=direct_frame(),
    diff=diff_frame(),
)

direct_writes = 0
diff_writes = 0
for l, r, val in updates:
    width = r - l + 1
    for i in range(l, r + 1):
        direct[i] += val
    diff[l] += val
    diff[r + 1] -= val
    direct_writes += width
    diff_writes += 2
    cell_word = "cell" if width == 1 else "cells"
    rec.step(
        f"Update [{l}, {r}] by {val}. The direct loop writes {width} {cell_word}, "
        f"{direct_writes} in total so far. diff writes diff[{l}] and diff[{r + 1}], "
        f"{diff_writes} in total so far.",
        direct=direct_frame(l, r),
        diff=diff_frame([l, r + 1]),
    )

built = []
current = 0
for i in range(n):
    current += diff[i]
    built.append(current)

rec.step(
    f"After {m} updates the direct loop made {direct_writes} writes; diff made {diff_writes} plus "
    f"one {n}-step rebuild, {diff_writes + n} in all. Both end at {built}.",
    direct=direct_frame(),
    diff=diff_frame(),
)

rec.output(" ".join(map(str, built)) + "\n")
